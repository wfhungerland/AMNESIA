"""Gewicht verdraengter Sektoren (Gutachten): US-Einfuhren aus Japan, Korea und China je Warengruppe,
aus UN Comtrade. SITC Rev. 1 AG3 (1962-1999), SITC Rev. 3 AG3 (1992-2009), HS AG4 (2008-2023, nur China).
Meldeland USA (841 bis 1980, danach 842). Ergebnis: data/raw/comtrade_us_imports_groups.csv
"""
import os
import json, time, urllib.request
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
API = ("https://comtradeapi.un.org/data/v1/get/C/A/{cl}?reporterCode={rep}&period={per}&partnerCode={par}&flowCode=M"
       "&cmdCode={ag}&motCode=0&partner2Code=0&customsCode=C00")
JOBS = [("S1", "AG3", p, range(1962, 2000)) for p in ("392", "410", "156")] + \
       [("S3", "AG3", p, range(1992, 2010)) for p in ("410", "156")] + [("HS", "AG4", "156", range(2008, 2024))]
rows = []
for cl, ag, par, yrs in JOBS:
    yrs = list(yrs)
    for rep in ("841", "842"):
        for i in range(0, len(yrs), 6):
            url = API.format(cl=cl, rep=rep, per=",".join(map(str, yrs[i:i + 6])), par=par, ag=ag)
            for t in range(5):
                try:
                    req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": os.environ.get("COMTRADE_KEY", "dummy")})
                    with urllib.request.urlopen(req, timeout=180) as r:
                        data = json.load(r).get("data", [])
                    rows += [{"cl": cl, "partner": int(par), "year": v["period"], "code": v["cmdCode"], "value": v["primaryValue"]} for v in data]
                    break
                except Exception:
                    time.sleep(4 * (t + 1))
            time.sleep(1.2)
d = pd.DataFrame(rows).drop_duplicates(["cl", "partner", "year", "code"])
d.to_csv(D / "raw" / "comtrade_us_imports_groups.csv", index=False)
print(d.groupby(["cl", "partner"]).year.agg(["min", "max", "count"]))
