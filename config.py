# ============ SETTINGS: yahan se apni marzi se tabdeeli karein ============
MAX_AGE_DAYS = 7        # itne din mein apply na karein to job khud hat jayegi
MIN_SCORE = 30          # isse kam score wali jobs na dikhayein
MIN_ALERT_SCORE = 60    # Telegram alert sirf isse zyada score par
ALLOW_POSSIBLE = True   # False = sirf wo jobs jin mein "sponsorship" likha ho

# ---------- Labour fields (job ke TITLE mein ye lafz hon to job li jayegi) ----------
FIELDS = {
 "Construction": ["construction", "mason", "bricklayer", "steel fixer", "scaffold", "concrete", "carpenter", "roofer", "tiler", "plasterer", "painter", "glazier", "bauhelfer", "maurer", "zimmerer", "malarz", "muratore", "operaio edile", "bouwvakker"],
 "Welding & Fabrication": ["welder", "welding", "fabricator", "pipe fitter", "fitter", "boilermaker", "schweißer", "schweisser", "spawacz", "saldatore", "lasser", "soldador", "shipyard"],
 "Electrical & Mechanical": ["electrician", "elektriker", "elektryk", "elettricista", "elektricien", "electricista", "mechanic", "mechaniker", "plumber", "installateur", "hydraulik", "idraulico", "hvac", "technician", "maintenance", "cnc"],
 "Driving & Transport": ["truck driver", "lorry driver", "delivery driver", "driver", "forklift", "fahrer", "kierowca", "autista", "chauffeur", "conductor", "courier", "kurier"],
 "Warehouse & Logistics": ["warehouse", "picker", "packer", "loader", "lagerhelfer", "lagermitarbeiter", "magazynier", "magazziniere", "magazijn", "mozo de almac", "logistics"],
 "Factory & Production": ["production worker", "machine operator", "assembly", "factory", "operator", "produktionshelfer", "produktionsmitarbeiter", "pracownik produkcji", "operaio", "productiemedewerker", "peón", "peon"],
 "Agriculture & Farm": ["farm", "harvest", "picker", "greenhouse", "agricultur", "gardener", "landscap", "erntehelfer", "gärtner", "saisonarbeiter", "rolnik", "bracciante", "fruit", "dairy", "poultry"],
 "Food Processing": ["meat", "slaughter", "butcher", "food processing", "fish processing", "bakery", "fleisch", "metzger", "ubojnia", "macellaio"],
 "Hospitality & Kitchen": ["cook", "chef", "kitchen", "dishwasher", "kitchen helper", "waiter", "housekeeping", "hotel", "küchenhilfe", "koch", "kucharz", "cuoco", "lavapiatti"],
 "Cleaning & Laundry": ["cleaner", "cleaning", "janitor", "laundry", "housekeeper", "reinigungskraft", "reinigung", "sprzątacz", "addetto pulizie", "schoonmaker"],
 "Care & Support": ["caregiver", "care assistant", "nursing assistant", "care worker", "pflegehelfer", "altenpflege", "opiekun", "badante", "oss", "zorgmedewerker"],
 "Security": ["security guard", "security officer", "sicherheitsmitarbeiter", "ochroniarz", "guardia"],
 "Textile & Tailoring": ["tailor", "sewing", "garment", "näher", "szwaczka", "sarto"],
 "Manufacturing Helpers": ["helper", "helfer", "pomocnik", "ausiliario", "general worker", "labourer", "laborer", "arbeiter"],
}

# ---------- Mulk: region, Adzuna code (agar available), note ----------
COUNTRIES = {
 # EUROPE
 "Germany":     {"region": "Europe", "adzuna": "de", "note": "Sab se bari demand: construction, driver, warehouse, care. Zyada jobs mein German zaroori."},
 "Poland":      {"region": "Europe", "adzuna": "pl", "note": "Factory, warehouse, driver. Pakistan ke sath labour agreement ki khabrein hain."},
 "Italy":       {"region": "Europe", "adzuna": "it", "note": "3 saal ka kota (decreto flussi): agriculture, tourism, shipbreaking, care. 10,500 jobs Pakistan ke liye."},
 "Netherlands": {"region": "Europe", "adzuna": "nl", "note": "Warehouse, greenhouse, logistics. Zyada tar agency ke zariye."},
 "Austria":     {"region": "Europe", "adzuna": "at", "note": "Skilled trades, tourism."},
 "Spain":       {"region": "Europe", "adzuna": "es", "note": "Agriculture (seasonal), tourism."},
 "Romania":     {"region": "Europe", "adzuna": None, "note": "Construction, agriculture, hospitality."},
 "Czechia":     {"region": "Europe", "adzuna": None, "note": "Factory, warehouse."},
 "Portugal":    {"region": "Europe", "adzuna": None, "note": "Agriculture, tourism, construction."},
 "Hungary":     {"region": "Europe", "adzuna": None, "note": "Factory, warehouse."},
 "Croatia":     {"region": "Europe", "adzuna": None, "note": "Construction, tourism."},
 "Lithuania":   {"region": "Europe", "adzuna": None, "note": "Driver, warehouse."},
 "Slovakia":    {"region": "Europe", "adzuna": None, "note": "Factory."},
 "Bulgaria":    {"region": "Europe", "adzuna": None, "note": "Factory, construction."},
 "Malta":       {"region": "Europe", "adzuna": None, "note": "Hospitality, care."},
 "Greece":      {"region": "Europe", "adzuna": None, "note": "Seasonal agriculture, tourism."},
 # ASIA
 "Singapore":   {"region": "Asia", "adzuna": "sg", "note": "Construction, marine/shipyard. Employer work permit deta hai; quota system."},
 "Japan":       {"region": "Asia", "adzuna": None, "note": "SSW visa: care, construction, farming, food, manufacturing."},
 "South Korea": {"region": "Asia", "adzuna": None, "note": "Manufacturing, farming (government EPS program)."},
 "Malaysia":    {"region": "Asia", "adzuna": None, "note": "Plantation, manufacturing, construction. Sirf approved channel se."},
 "Taiwan":      {"region": "Asia", "adzuna": None, "note": "Factory, caretaker."},
 "UAE":         {"region": "Asia", "adzuna": None, "note": "Construction, hospitality, security, driver. Employer visa deta hai."},
 "Saudi Arabia":{"region": "Asia", "adzuna": None, "note": "Construction, driver, hospitality."},
 "Qatar":       {"region": "Asia", "adzuna": None, "note": "Construction, hospitality, security."},
 "Oman":        {"region": "Asia", "adzuna": None, "note": "Construction, hospitality."},
 "Kuwait":      {"region": "Asia", "adzuna": None, "note": "Construction, domestic, hospitality."},
 "Bahrain":     {"region": "Asia", "adzuna": None, "note": "Construction, hospitality."},
}

# Adzuna par har mulk ki apni zubaan mein search
ADZUNA_QUERIES = {
 "de": "Schweißer Elektriker Lagerhelfer Produktionshelfer Fahrer Bauhelfer Reinigungskraft Küchenhilfe Erntehelfer Pflegehelfer Visum",
 "at": "Schweißer Elektriker Lagerhelfer Produktionshelfer Fahrer Bauhelfer Reinigungskraft Küchenhilfe Erntehelfer",
 "pl": "spawacz elektryk magazynier operator kierowca pracownik produkcji murarz pomocnik sprzątacz",
 "it": "saldatore elettricista magazziniere operaio autista muratore bracciante addetto pulizie",
 "nl": "lasser elektricien magazijnmedewerker productiemedewerker chauffeur schoonmaker",
 "es": "soldador electricista mozo almacén peón conductor albañil limpieza",
 "sg": "welder electrician technician operator driver cleaner construction worker",
}

# ---------- Sponsorship ki nishaniyan ----------
SPONSOR_WORDS = ["visa sponsorship", "visa sponsor", "sponsorship available", "we sponsor", "will sponsor", "sponsor your visa",
                 "work permit provided", "work permit will be", "we arrange the visa", "visum", "visasponsoring", "arbeitserlaubnis wird",
                 "relocation", "umzugshilfe", "international candidates", "foreign workers", "ausländische", "cudzoziem", "cittadini extracomunitari"]
EXTRA_PERKS = ["accommodation", "housing provided", "unterkunft", "wohnung", "zakwaterowanie", "alloggio", "travel costs", "flight"]
# Inme se kuch likha ho to job REJECT (sponsorship nahi milegi)
NO_SPONSOR_WORDS = ["no visa sponsorship", "no sponsorship", "cannot sponsor", "unable to sponsor", "eu citizens only", "eu citizenship required",
                    "must have the right to work", "right to work in the", "nur eu", "eu-bürger", "ohne visum"]
# Language ki shart (score kam hota hai)
LANGUAGE_REQUIRED = ["deutsch c1", "deutsch b2", "fließend deutsch", "verhandlungssicher", "muttersprache", "fluent german", "fluent polish", "fluent italian", "flüssig deutsch"]
# SCAM ki nishaniyan: inme se kuch bhi ho to job turant reject
SCAM_WORDS = ["registration fee", "visa fee", "processing fee", "pay to apply", "send money", "advance payment", "security deposit",
              "agent fee", "whatsapp only", "guaranteed visa", "100% visa", "no interview"]
