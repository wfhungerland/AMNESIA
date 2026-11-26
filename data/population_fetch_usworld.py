"""Referee round 3: US imports from the world by SITC Rev. 1 three-digit group, 1962-1999, from UN Comtrade.
Used for a measure of US comparative disadvantage that does not depend on the challenger.
Reporter USA (841 to 1980, 842 afterwards). Output: data/raw/comtrade_us_imports_world_s1.csv
"""
import json
import os
import time
import urllib.request
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
API = ("https://comtradeapi.un.org/data/v1/get/C/A/S1?reporterCode={rep}&period={per}&partnerCode=0&flowCode=M"
       "&cmdCode=AG3&motCode=0&partner2Code=0&customsCode=C00")
rows = []
yrs = list(range(1962, 2000))
for rep in ("841", "842"):
    for i in range(0, len(yrs), 6):
        url = API.format(rep=rep, per=",".join(map(str, yrs[i:i + 6])))
        for t in range(5):
            try:
                req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": os.environ.get("COMTRADE_KEY", "dummy")})
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = json.load(r).get("data", [])
                rows += [{"reporter": int(rep), "year": v["period"], "code": v["cmdCode"], "value": v["primaryValue"]} for v in data]
                break
            except Exception as e:
                print("retry", rep, yrs[i], e)
                time.sleep(4 * (t + 1))
        time.sleep(1.2)
d = pd.DataFrame(rows).drop_duplicates(["year", "code"])
(D / "raw").mkdir(exist_ok=True)
d.to_csv(D / "raw" / "comtrade_us_imports_world_s1.csv", index=False)
print(d.groupby("reporter").year.agg(["min", "max", "count"]))
