"""Population verdraengter Sektoren (Gutachten Befund 1): Weltausfuhren nach SITC Rev. 1, 3-Steller,
fuer Japan, Korea, China und die USA, 1962-2023, aus UN Comtrade (Aggregatebene AG3).
Ergebnis: data/raw/comtrade_s1_ag3.csv
"""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
API = ("https://comtradeapi.un.org/data/v1/get/C/A/S1?reporterCode={rep}&period={per}&partnerCode=0&flowCode=X"
       "&cmdCode=AG3&motCode=0&partner2Code=0&customsCode=C00")
rows = []
for rep in ["392", "410", "156", "841", "842"]:
    years = list(range(1962, 2024))
    for i in range(0, len(years), 6):
        url = API.format(rep=rep, per=",".join(map(str, years[i:i + 6])))
        for t in range(5):
            try:
                req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": "dummy"})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = json.load(r).get("data", [])
                rows += [{"reporter": v["reporterCode"], "year": v["period"], "sitc3": v["cmdCode"], "value": v["primaryValue"]} for v in data]
                break
            except Exception:
                time.sleep(4 * (t + 1))
        time.sleep(1.2)
d = pd.DataFrame(rows)
d.to_csv(D / "raw" / "comtrade_s1_ag3.csv", index=False)
print(d.groupby("reporter").year.agg(["min", "max", "count"]))
