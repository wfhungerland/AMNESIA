"""Feste Woerterlisten der Kongressmessung (Congressional Record 1995-2025), analog zu hansard_salience.py.

ECON: Wirtschaftsdebatte, wenn der Granule-Titel einen dieser Wortstaemme enthaelt (Kleinschreibung).
Die Liste folgt econ_v2 der Hansard-Messung (Handel, Zoelle, Industrie, Sektoren) und ergaenzt
die Begriffe der Zeit nach 1995 (WTO, NAFTA, Normal Trade Relations, Waehrung, Auslagerung).
Nicht enthalten: Haushalt, Steuern allgemein, Arbeitsmarkt allgemein ("jobs"), Energie allgemein.
"""
import re

FILTER_VERSION = "crec_econ_v1"
ECON = ["trade", "tariff", "commerc", "import(?!an)", "export", "duties", "customs", "manufactur",
        "industr", "dumping", "subsid", "competitiv", "competition", "outsourc", "offshor", "currenc",
        "buy american", "made in america", "most favored", "normal trade relations", "wto",
        "world trade organization", "nafta", "gatt", "steel", "alumin", "textile", "apparel",
        "furniture", "solar", "semiconductor", "microchip", "chips act", "telecommunic", "huawei", "zte",
        "automo", "auto industry", "automaker", "electric vehicle", "shipbuild", "rare earth",
        "critical mineral", "supply chain", "intellectual property", "patent", "counterfeit",
        # Sektorwoerter aller Feinsektoren (SECTORS unten), damit kein Sektor ueber den Titel bevorzugt wird
        "chemical", "pharmaceutic", "paper", "lumber", "tire", "rubber", "plastic", "footwear", "shoe",
        "toy", "glass", "ceramic", "washer", "washing machine", "appliance", "computer", "machine tool",
        "battery", "batteries", "electronic", "telecom", "broadband", "5g", "vehicle", "cars", "honey",
        "shrimp", "garlic", "catfish", "magnet", "drone"]
# Wortanfang erzwungen (nicht "retire", "important"); "cars" und "zte" nur als ganzes Wort.
_ECON = re.compile(r"\b(" + "|".join(w if "(" in w else re.escape(w) for w in ECON) + ")", re.I)
_WHOLE = {"cars", "zte", "wto", "gatt", "5g"}
ECON_RX = re.compile(r"\b(" + "|".join(w if "(" in w else re.escape(w) for w in ECON if w not in _WHOLE)
                     + r")|\b(" + "|".join(_WHOLE) + r")\b", re.I)


def is_econ(title):
    return bool(ECON_RX.search(title or ""))


# Nennung des Ziellands im Volltext (Wortgrenzen). "Republic of China" (Taiwan) wird vorher entfernt.
TARGET = re.compile(r"\b(china|chinese|prc|beijing|people's republic)\b", re.I)
TAIWAN = re.compile(r"(?<!people's )\brepublic of china\b", re.I)
BENCH = {"japan": re.compile(r"\b(japan|japanese)\b", re.I),
         "mexico": re.compile(r"\b(mexico|mexican)\b", re.I)}
# Wettbewerbswoerter wie hansard_competition.py, ergaenzt um Waehrung und Auslagerung.
COMP = re.compile(r"^(competition|competitor|competitors|compete|competing|dumping|dumped|unfair|"
                  r"subsid\w*|undersell\w*|cheap|cheaper|imitat\w*|rival\w*|manipulat\w*|overcapacity|"
                  r"outsourc\w*|offshor\w*|counterfeit\w*)$", re.I)
TWORD = re.compile(r"^(china|chinese|prc|beijing|china's)$", re.I)

# Sektorwoerter (einzelne Woerter, nach Entfernen von Satzzeichen). Gruppen passen zu HS-Kapiteln
# (HS2) und SITC-Abteilungen (S2), damit die Messung an data/population_weight.csv anschliesst.
SECT = {
    "steel_metals": (r"^(steel|iron|alumin(i)?um|copper|nickel|magnesium|tungsten|metals?)$",
                     ["72", "73", "74", "75", "76", "78", "79", "80", "81"], ["67", "68", "69"]),
    "chemicals": (r"^(chemicals?|pharmaceuticals?|fertili[sz]ers?|glyphosate|citric)$",
                  ["28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38"], ["51", "52", "53", "54", "55", "56", "57", "58", "59"]),
    "plastics_rubber": (r"^(plastics?|rubber|tires?|tyres?)$", ["39", "40"], ["62"]),
    "paper_wood": (r"^(paper|paperboard|pulp|lumber|plywood|wood|timber)$", ["44", "45", "46", "47", "48", "49"], ["63", "64"]),
    "textiles_apparel": (r"^(textiles?|apparel|garments?|clothing|cotton|yarn|fabrics?|footwear|shoes)$",
                         [str(i) for i in range(50, 68)], ["61", "65", "83", "84", "85"]),
    "minerals_glass": (r"^(glass|ceramics?|cement|stone|granite|tiles?|graphite)$", ["68", "69", "70"], ["66"]),
    "jewelry": (r"^(jewelry|jewellery|pearls?|gems?)$", ["71"], ["97"]),
    "tools_hardware": (r"^(tools|hardware|nails|fasteners|cutlery|locks)$", ["82", "83"], []),
    "machinery": (r"^(machinery|machines|machine-tools?|computers?|robots?|robotics|turbines?)$", ["84"], ["71", "72", "73", "74", "75"]),
    "electronics": (r"^(electronics?|semiconductors?|chips?|microchips?|solar|batteries|telecommunications?|"
                    r"huawei|zte|5g|televisions?|electrical)$", ["85"], ["76", "77"]),
    "vehicles": (r"^(automobiles?|autos?|cars|vehicles?|automakers?|ev|evs|trucks?|bicycles?)$", ["86", "87", "88", "89"], ["78", "79"]),
    "instruments": (r"^(instruments?|optical|medical-devices?|watches|clocks)$", ["90", "91", "92"], ["87", "88"]),
    "furniture_toys": (r"^(furniture|mattresses?|toys?|lighting|lamps?)$", ["94", "95", "96"], ["82", "89"]),
}
SECT_RX = {k: re.compile(v[0], re.I) for k, v in SECT.items()}


def sector_of(data, code):
    """Sektorgruppe einer Warengruppe aus population_weight.csv (hs4 oder s3)."""
    code = str(code)
    for k, (_, hs2, s2) in SECT.items():
        if data == "hs4" and code[:2] in hs2:
            return k
        if data == "s3" and code[:2] in s2:
            return k
    return None


# Feinsektoren fuer den Sektortest (crec_sectors.py): Sektorwoerter (ganze Woerter nach Entfernen von
# Satzzeichen), Warengruppen als Praefixe in HS4 und SITC Rev. 3 (wie in data/population_crossovers.csv).
FINE = {
    "steel": (r"^(steel|steelworkers|steelmakers|steelmaking|steelworker)$", ["72", "7301", "7302", "7303", "7304", "7305", "7306"], ["67"]),
    "aluminium": (r"^(aluminum|aluminium)$", ["76"], ["684"]),
    "solar": (r"^(solar|photovoltaic|photovoltaics)$", ["8541"], []),
    "washers": (r"^(washers|washing)$", ["8450"], ["775"]),
    "telecom": (r"^(huawei|zte|telecommunications|telecom|5g|routers)$", ["8517"], ["764"]),
    "semiconductors": (r"^(semiconductor|semiconductors|chip|chips|microchip|microchips|chipmakers)$", ["8542", "8486"], ["776"]),
    "cars": (r"^(automobile|automobiles|automaker|automakers|cars|autos|vehicle|vehicles|ev|evs)$", ["8703"], ["781"]),
    "furniture": (r"^(furniture|bedroom|mattress|mattresses)$", ["9401", "9403", "9404"], ["821"]),
    "textiles_apparel": (r"^(textile|textiles|apparel|garment|garments|clothing|yarn|fabric|fabrics)$",
                         [str(i) for i in range(50, 64)], ["65", "84"]),
    "footwear": (r"^(footwear|shoe|shoes)$", ["64"], ["851"]),
    "toys": (r"^(toy|toys)$", ["9503"], ["894"]),
    "tires": (r"^(tire|tires|tyre|tyres)$", ["4011"], ["625"]),
    "paper": (r"^(paperboard|pulp|newsprint|papermakers|papermaking)$", ["47", "48"], ["64"]),
    "chemicals": (r"^(chemical|chemicals)$", ["28", "29"], ["51", "52"]),
    "computers": (r"^(computer|computers|laptops|laptop|pcs)$", ["8471"], ["752"]),
    "glass_ceramics": (r"^(glass|glassware|ceramic|ceramics|tile|tiles)$", ["69", "70"], ["664", "665", "666"]),
    "batteries": (r"^(battery|batteries|lithium-ion)$", ["8506", "8507"], ["778"]),
}
FINE_RX = {k: re.compile(v[0], re.I) for k, v in FINE.items()}


def fine_of(data, code):
    code = str(code)
    for k, (_, hs, s3) in FINE.items():
        if any(code.startswith(p) for p in (hs if data == "hs4" else s3)):
            return k
    return None


# Fall Japan im gebundenen Record (crecb_salience.py): Zielland, Vergleichslaender, Sektoren mit SITC Rev. 1.
JWORD = re.compile(r"^(japan|japanese|japan's)$", re.I)
GWORD = re.compile(r"^(germany|german|germany's)$", re.I)
CWORD = TWORD
JP_FINE = {
    "textiles": (r"^(textile|textiles|apparel|cotton|wool|woolen|yarn|fabric|fabrics|garment|garments|clothing)$", ["65", "841"]),
    "steel": (r"^(steel|steelworkers|steelmakers|steelmaking)$", ["67"]),
    "televisions": (r"^(television|televisions|tv|tvs)$", ["724"]),
    "cars": (r"^(automobile|automobiles|automaker|automakers|cars|autos|motorcycles)$", ["732"]),
    "semiconductors": (r"^(semiconductor|semiconductors|chip|chips|microchip|microchips)$", ["729"]),
    "machine_tools": (r"^(machine-tool|machine-tools)$", ["715"]),
    "ships": (r"^(shipbuilding|shipyard|shipyards|shipbuilders)$", ["735"]),
    "footwear": (r"^(footwear|shoe|shoes)$", ["851"]),
    "cameras": (r"^(camera|cameras|optical)$", ["861"]),
    "toys": (r"^(toy|toys)$", ["894"]),
    "glass_ceramics": (r"^(glass|glassware|ceramic|ceramics|pottery|chinaware|tile|tiles)$", ["664", "665", "666"]),
    "bearings": (r"^(bearings|ball-bearings)$", ["719"]),
    "tires": (r"^(tire|tires|tyre|tyres)$", ["629"]),
    "plywood": (r"^(plywood|veneer)$", ["631"]),
}
JP_FINE_RX = {k: re.compile(v[0], re.I) for k, v in JP_FINE.items()}


def jp_fine_of(code):
    code = str(code)
    for k, (_, pre) in JP_FINE.items():
        if any(code.startswith(p) for p in pre):
            return k
    return None
