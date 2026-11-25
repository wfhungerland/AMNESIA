"""Export-Meilensteine 1962-2024 aus UN Comtrade: erstes Jahr, in dem die Weltausfuhren des Aufsteigers
die des Etablierten erreichen oder uebersteigen (Verhaeltnis >= 1).

Je Sektor: Klassifikation, Warencode, Aufsteiger, Etablierter. Werte: Ausfuhren an die Welt (partner 0),
laufende US-Dollar, wie vom Ausfuhrland gemeldet. Ergebnis: data/ds1_export_series.csv und
data/ds1_export_milestones.csv. Der API-Schluessel wird vom Sitzungs-Proxy eingesetzt.
"""
import os
import json
import time
import urllib.request
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
API = "https://comtradeapi.un.org/data/v1/get/C/A/{cl}?reporterCode={rep}&period={per}&partnerCode=0&flowCode=X&cmdCode={cmd}&motCode=0&partner2Code=0&customsCode=C00"
# Comtrade-Codes: 392 Japan, 410 Korea, 156 China, 841/842 USA (841 bis 1980, 842 danach), 276/280 Deutschland
US = "841,842"
DE = "276,280"
SECTORS = [
    # id, Aufsteiger, Etablierter, Klassifikation, Code, Jahre, Beschreibung
    ("JP-STEEL", "392", US, "S1", "67", range(1962, 1976), "Iron and steel (SITC 67), Japan vs US"),
    ("JP-TV", "392", US, "S1", "7241", range(1962, 1981), "Television receivers (SITC 7241), Japan vs US"),
    ("JP-AUTO", "392", US, "S1", "7321", range(1962, 1988), "Passenger cars (SITC 7321), Japan vs US"),
    ("JP-SEMI", "392", US, "S2", "776", range(1976, 1995), "Valves, transistors, microcircuits (SITC 776), Japan vs US"),
    ("KR-SEMI", "410", US, "S2", "776", range(1976, 2005), "Valves, transistors, microcircuits (SITC 776), Korea vs US"),
    ("KR-SHIP", "410", "392", "S2", "793", range(1976, 2023), "Ships and boats (SITC 793), Korea vs Japan"),
    ("KR-SHIP-HS", "410", "392", "HS", "89", range(1996, 2023), "Ships and boats (HS 89), Korea vs Japan; SITC Rev.2 series ends 2000"),
    ("CN-MFG", "156", US, "S3", "5,6,7,8", range(1988, 2016), "Manufactures (SITC 5-8, incl. 68), China vs US"),
    ("CN-SOLAR", "156", DE, "HS", "854140", range(2002, 2017), "Photosensitive devices incl. PV cells (HS 854140), China vs Germany"),
    ("CN-TEL", "156", US, "HS", "8517", range(2002, 2017), "Telephone and telecom apparatus (HS 8517), China vs US"),
    ("CN-EV", "156", DE, "HS", "870380", range(2017, 2025), "Electric passenger cars (HS 870380), China vs Germany"),
    ("CN-CHIP", "156", US, "HS", "8542", range(2017, 2025), "Integrated circuits (HS 8542), China vs US"),
]


def get(cl, rep, years, cmd):
    rows = []
    ys = list(years)
    for i in range(0, len(ys), 10):
        url = API.format(cl=cl, rep=rep, per=",".join(map(str, ys[i:i + 10])), cmd=cmd)
        for t in range(4):
            try:
                req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": os.environ.get("COMTRADE_KEY", "dummy")})
                with urllib.request.urlopen(req, timeout=120) as r:
                    rows += json.load(r).get("data", [])
                break
            except Exception:
                time.sleep(3 * (t + 1))
        time.sleep(1.2)
    return rows


series, ms = [], []
for sid, ch, inc, cl, cmd, years, desc in SECTORS:
    for role, rep in (("challenger", ch), ("incumbent", inc)):
        for r in get(cl, rep, years, cmd):
            series.append({"sector": sid, "role": role, "reporter": r["reporterCode"], "year": int(r["period"]),
                           "cmd": r["cmdCode"], "value_usd": r["primaryValue"], "classification": cl})
s = pd.DataFrame(series)
s.to_csv(D / "ds1_export_series.csv", index=False)
w = s.groupby(["sector", "year", "role"]).value_usd.sum().unstack("role")
for sid, ch, inc, cl, cmd, years, desc in SECTORS:
    if sid not in w.index.get_level_values(0):
        ms.append({"sector": sid, "description": desc, "first_year": None, "crossover_year": None, "ratio_first_year": None, "note": "keine Daten"})
        continue
    x = w.loc[sid].dropna()
    ratio = x.challenger / x.incumbent
    cross = ratio[ratio >= 1]
    ms.append({"sector": sid, "description": desc, "first_year": int(x.index.min()),
               "crossover_year": int(cross.index.min()) if len(cross) else None,
               "ratio_first_year": round(float(ratio.iloc[0]), 3), "ratio_last_year": round(float(ratio.iloc[-1]), 3),
               "note": "bereits im ersten Datenjahr vorn" if ratio.iloc[0] >= 1 else ""})
m = pd.DataFrame(ms)
m.to_csv(D / "ds1_export_milestones.csv", index=False)
print(m.to_string(index=False))
