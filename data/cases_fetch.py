"""Weitere Faelle (Gegenfaelle und neue Verdraengungsfaelle gegen die USA): Weltausfuhren nach Warengruppe aus UN Comtrade.

Aufsteiger: Thailand (764), Vietnam (704), Malaysia (458), Mexiko (484), Brasilien (76), Hongkong (344),
Taiwan (490 "Other Asia, nes"); Etablierter: USA (841 bis 1980, 842).
- Direkt gemeldete Ausfuhren (partnerCode=0): SITC Rev. 1 AG3 1962-1999, SITC Rev. 3 AG3 1992-2009, HS AG4 2008-2023.
- Taiwan meldet in SITC nicht selbst. Spiegeldaten: Einfuhren aller Meldelaender aus 490 und, gleich bewertet,
  aus den USA (841, 842), SITC Rev. 1 AG3 1962-1999 und SITC Rev. 3 AG3 1992-2009. Code 490 kann Restposten
  anderer asiatischer Gebiete enthalten; Taiwan dominiert ihn (zu pruefen je Jahr, siehe cases_test.py).
- Hongkong meldet unter X auch Wiederausfuhren (vor allem chinesischer Waren); abgezogen werden die
  Wiederausfuhren (flowCode RX, Modus hkrx), damit nur Hongkongs eigene Ausfuhren zaehlen.
- US-Einfuhren aus jedem Aufsteiger (Heimatmarkt), gleiche Klassifikationen.
Ergebnis: data/raw/cases_exports.csv, data/raw/cases_mirror_tw.csv, data/raw/cases_us_imports.csv,
data/raw/cases_hk_reexports.csv
Aufruf: python3 data/cases_fetch.py [exports|mirror|usimports|hkrx]
"""
import json, sys, time, urllib.request
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
BASE = "https://comtradeapi.un.org/data/v1/get/C/A/{cl}?{q}&motCode=0&partner2Code=0&customsCode=C00"
NEW = ["764", "704", "458", "484", "76", "344"]
CLS = [("S1", "AG3", range(1962, 2000), 6), ("S3", "AG3", range(1992, 2010), 6), ("HS", "AG4", range(2008, 2024), 2)]


def get(cl, q):
    url = BASE.format(cl=cl, q=q)
    for t in range(6):
        try:
            req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": "dummy"})
            with urllib.request.urlopen(req, timeout=240) as r:
                d = json.load(r)
            time.sleep(1.2)
            return d.get("data", []) or []
        except Exception as e:
            print("retry", t, cl, q[:80], type(e).__name__, flush=True)
            time.sleep(5 * (t + 1))
    print("FEHLER", cl, q, flush=True)
    return []


def rows(data, cl):
    return [{"cl": cl, "reporter": v["reporterCode"], "partner": v["partnerCode"], "year": v["period"],
             "code": v["cmdCode"], "value": v["primaryValue"]} for v in data]


what = sys.argv[1] if len(sys.argv) > 1 else "exports"
out = []
if what == "exports":
    for cl, ag, yrs, step in CLS:
        reps = NEW + ["841", "842"] + (["490"] if cl == "HS" else [])
        yrs = list(yrs)
        for rep in reps:
            for i in range(0, len(yrs), step):
                per = ",".join(map(str, yrs[i:i + step]))
                out += rows(get(cl, f"reporterCode={rep}&period={per}&partnerCode=0&flowCode=X&cmdCode={ag}"), cl)
            print(cl, rep, len(out), flush=True)
    f = "cases_exports.csv"
elif what == "mirror":
    for cl, ag, yrs, _ in CLS[:2]:
        for y in yrs:
            for par in ("490", "842", "841"):
                out += rows(get(cl, f"period={y}&partnerCode={par}&flowCode=M&cmdCode={ag}"), cl)
            print(cl, y, len(out), flush=True)
    f = "cases_mirror_tw.csv"
elif what == "hkrx":
    for cl, ag, yrs, step in CLS:
        yrs = list(yrs)
        for i in range(0, len(yrs), step):
            per = ",".join(map(str, yrs[i:i + step]))
            out += rows(get(cl, f"reporterCode=344&period={per}&partnerCode=0&flowCode=RX&cmdCode={ag}"), cl)
        print(cl, len(out), flush=True)
    f = "cases_hk_reexports.csv"
else:
    for cl, ag, yrs, step in CLS:
        yrs = list(yrs)
        for par in NEW + ["490"]:
            for rep in ("841", "842"):
                for i in range(0, len(yrs), step):
                    per = ",".join(map(str, yrs[i:i + step]))
                    out += rows(get(cl, f"reporterCode={rep}&period={per}&partnerCode={par}&flowCode=M&cmdCode={ag}"), cl)
            print(cl, par, len(out), flush=True)
    f = "cases_us_imports.csv"
d = pd.DataFrame(out)
d.to_csv(D / "raw" / f, index=False)
print(d.groupby(["cl", "reporter"]).year.agg(["min", "max", "count"]).to_string() if what != "mirror" else d.groupby(["cl", "partner"]).year.agg(["min", "max", "count"]).to_string())
