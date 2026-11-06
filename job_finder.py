"""Labour Job Finder: jobs dhoondta hai, filter+score karta hai, docs/jobs.json mein save karta hai."""
import hashlib, json, os, re, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone

import config as C

OUT = os.path.join("docs", "jobs.json")
NOW = datetime.now(timezone.utc)
FIELD_RX = {f: re.compile(r"\b(" + "|".join(map(re.escape, k)) + ")", re.I) for f, k in C.FIELDS.items()}
CODE_TO_COUNTRY = {v["adzuna"]: n for n, v in C.COUNTRIES.items() if v["adzuna"]}


def get_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "labour-job-finder/1.0"})
    with urllib.request.urlopen(req, timeout=25) as r:
        return json.loads(r.read().decode("utf-8"))


def clean(s):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s or "")).strip()


def parse_date(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


# ---------------- Sources ----------------
def from_arbeitnow():
    out = []
    for page in (1, 2, 3):
        try:
            data = get_json(f"https://www.arbeitnow.com/api/job-board-api?page={page}")
        except Exception as e:
            print("Arbeitnow error:", e)
            break
        for j in data.get("data", []):
            ts = j.get("created_at")
            out.append(dict(title=j.get("title", ""), company=j.get("company_name", ""), location=j.get("location", ""),
                            country="Germany", url=j.get("url", ""), source="Arbeitnow",
                            text=clean(j.get("description")) + " " + " ".join(j.get("tags", [])),
                            posted=datetime.fromtimestamp(ts, timezone.utc) if ts else None))
    return out


def from_adzuna():
    app_id, app_key = os.getenv("ADZUNA_APP_ID"), os.getenv("ADZUNA_APP_KEY")
    if not (app_id and app_key):
        print("Adzuna keys nahi milin, is source ko skip kar raha hoon.")
        return []
    out = []
    for code, query in C.ADZUNA_QUERIES.items():
        qs = urllib.parse.urlencode(dict(app_id=app_id, app_key=app_key, results_per_page=50,
                                         what_or=query, max_days_old=7, sort_by="date"))
        try:
            data = get_json(f"https://api.adzuna.com/v1/api/jobs/{code}/search/1?{qs}")
        except Exception as e:
            print(f"Adzuna {code} error:", e)
            continue
        for j in data.get("results", []):
            out.append(dict(title=j.get("title", ""), company=(j.get("company") or {}).get("display_name", ""),
                            location=(j.get("location") or {}).get("display_name", ""),
                            country=CODE_TO_COUNTRY.get(code, code.upper()), url=j.get("redirect_url", ""),
                            source="Adzuna", text=clean(j.get("description")), posted=parse_date(j.get("created", ""))))
    return out


# ---------------- Filter + Score ----------------
def evaluate(j):
    field = next((f for f, rx in FIELD_RX.items() if rx.search(j["title"])), None)
    if not field or not j["url"].startswith("http"):
        return None
    text = f'{j["title"]} {j["text"]}'.lower()
    if any(w in text for w in C.SCAM_WORDS) or any(w in text for w in C.NO_SPONSOR_WORDS):
        return None
    score, reasons = 10, []
    sponsor = any(w in text for w in C.SPONSOR_WORDS)
    if sponsor:
        score += 40
        reasons.append("Sponsorship/relocation likha hai")
    if any(w in text for w in C.EXTRA_PERKS):
        score += 10
        reasons.append("Rehaish ya safar ka zikr")
    if j["posted"]:
        hours = (NOW - j["posted"]).total_seconds() / 3600
        if hours <= 24:
            score += 20; reasons.append("Bilkul nayi (24 ghante)")
        elif hours <= 72:
            score += 12; reasons.append("Nayi (3 din)")
        elif hours <= 168:
            score += 5
    if any(w in text for w in C.LANGUAGE_REQUIRED):
        score -= 20
        reasons.append("Zubaan ki shart (German/Polish wagaira)")
    if C.COUNTRIES.get(j["country"], {}).get("note"):
        score += 10
    if not sponsor and not C.ALLOW_POSSIBLE:
        return None
    score = max(0, min(100, score))
    if score < C.MIN_SCORE:
        return None
    key = re.sub(r"\W+", "", f'{j["title"]}{j["company"]}{j["location"]}'.lower())
    return dict(id=hashlib.sha1(key.encode()).hexdigest()[:12], title=j["title"], company=j["company"],
                location=j["location"], country=j["country"], region=C.COUNTRIES.get(j["country"], {}).get("region", ""),
                field=field, url=j["url"], source=j["source"], score=score, sponsor=sponsor, reasons=reasons,
                posted=j["posted"].isoformat() if j["posted"] else None)


def notify(new_jobs):
    token, chat = os.getenv("TELEGRAM_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    top = sorted([j for j in new_jobs if j["score"] >= C.MIN_ALERT_SCORE], key=lambda j: -j["score"])[:10]
    if not (token and chat and top):
        return
    lines = [f'{len(top)} nayi jobs mili:'] + [f'\n{j["title"]} | {j["company"]} | {j["country"]} | score {j["score"]}\n{j["url"]}' for j in top]
    body = urllib.parse.urlencode(dict(chat_id=chat, text="\n".join(lines)[:4000], disable_web_page_preview="true")).encode()
    try:
        urllib.request.urlopen(f"https://api.telegram.org/bot{token}/sendMessage", body, timeout=20)
    except Exception as e:
        print("Telegram error:", e)


def main():
    try:
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
    except Exception:
        old = {}
    jobs = {j["id"]: j for j in old.get("jobs", [])}
    expired = old.get("expired", {})

    raw = from_arbeitnow() + from_adzuna()
    new_jobs = []
    for r in raw:
        j = evaluate(r)
        if not j or j["id"] in expired:
            continue
        if j["id"] in jobs:
            j["first_seen"] = jobs[j["id"]]["first_seen"]
        else:
            j["first_seen"] = NOW.isoformat()
            new_jobs.append(j)
        jobs[j["id"]] = j

    # 7 din se purani jobs hatao (aur dobara na aayein, isliye expired list mein yaad rakho)
    for jid, j in list(jobs.items()):
        if NOW - parse_date(j["first_seen"]) > timedelta(days=C.MAX_AGE_DAYS):
            expired[jid] = NOW.isoformat()
            del jobs[jid]
    expired = {k: v for k, v in expired.items() if NOW - parse_date(v) < timedelta(days=60)}

    result = dict(updated=NOW.isoformat(), max_age_days=C.MAX_AGE_DAYS,
                  countries=sorted(C.COUNTRIES), fields=sorted(C.FIELDS),
                  jobs=sorted(jobs.values(), key=lambda j: -j["score"]), expired=expired)
    os.makedirs("docs", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"Raw: {len(raw)} | Pending: {len(jobs)} | Nayi: {len(new_jobs)}")
    notify(new_jobs)


if __name__ == "__main__":
    main()
