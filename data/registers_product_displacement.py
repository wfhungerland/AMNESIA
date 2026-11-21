"""Ebene passt zu Ebene: Gingen US-Antidumpingverfahren gegen China (1996-2015) eine Verdraengung auf
Produktebene voraus? Mass: Chinas Anteil an den US-Einfuhren der HS6-Produkte des Verfahrens,
im Jahr vor der Einleitung (t-1) gegen vier Jahre vorher (t-4). Quelle: UN Comtrade (Meldeland USA,
Einfuhren, Partner Welt und China), TTBD fuer Verfahren und Warencodes.
Ergebnis: data/ds1_product_displacement.csv und Zusammenfassung auf der Konsole.
"""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
x = pd.read_excel(D / "raw/ttbd/gad/GAD/GAD-USA.xls", sheet_name=None)
m, p = x["AD-USA-Master"], x["AD-USA-Products"]
c = m[m.INV_CTY_CODE == "CHN"].copy()
c["y"] = pd.to_datetime(c.INIT_DATE, errors="coerce").dt.year
c = c[(c.y >= 1996) & (c.y <= 2015)]
pp = p[p.CASE_ID.isin(c.CASE_ID)].copy()
pp["hs6"] = pp.HS_CODE.astype(str).str.replace(".", "", regex=False).str[:6]
pp = pp[pp.hs6.str.len() == 6]
codes = sorted(pp.hs6.unique())
API = ("https://comtradeapi.un.org/data/v1/get/C/A/HS?reporterCode=842&period={y}&partnerCode=0,156&flowCode=M"
       "&cmdCode={cmd}&motCode=0&partner2Code=0&customsCode=C00")
cache = D / "raw" / "comtrade_us_imports_hs6.csv"
if cache.exists():
    imp = pd.read_csv(cache, dtype={"hs6": str})
else:
    rows = []
    for y in range(1992, 2015):
        for i in range(0, len(codes), 40):
            url = API.format(y=y, cmd=",".join(codes[i:i + 40]))
            for t in range(4):
                try:
                    req = urllib.request.Request(url, headers={"Ocp-Apim-Subscription-Key": "dummy"})
                    with urllib.request.urlopen(req, timeout=120) as r:
                        for v in json.load(r).get("data", []):
                            rows.append({"year": v["period"], "hs6": v["cmdCode"], "partner": v["partnerCode"], "value": v["primaryValue"]})
                    break
                except Exception:
                    time.sleep(3 * (t + 1))
            time.sleep(1.1)
    imp = pd.DataFrame(rows)
    imp.to_csv(cache, index=False)
imp["year"] = imp.year.astype(int)
w = imp.pivot_table(index=["hs6", "year"], columns="partner", values="value", aggfunc="sum").reset_index()
w.columns = ["hs6", "year", "world", "china"] if list(w.columns[2:]) == [0, 156] else list(w.columns)
res = []
for cid, g in pp.groupby("CASE_ID"):
    y0 = int(c.loc[c.CASE_ID == cid, "y"].iloc[0])
    sub = w[w.hs6.isin(g.hs6)]
    def share(yr):
        s = sub[sub.year == yr]
        return s.china.sum() / s.world.sum() if s.world.sum() > 0 else None
    a, b = share(y0 - 4), share(y0 - 1)
    res.append({"case_id": cid, "init_year": y0, "share_t4": a, "share_t1": b})
r = pd.DataFrame(res).dropna()
r["change_pp"] = 100 * (r.share_t1 - r.share_t4)
r.to_csv(D / "ds1_product_displacement.csv", index=False)
print(f"Faelle mit Daten: {len(r)}; Anteil mit steigendem China-Anteil: {(r.change_pp > 0).mean():.2f}; "
      f"Median Anteil t-4 {r.share_t4.median():.2f}, t-1 {r.share_t1.median():.2f}; Median Zuwachs {r.change_pp.median():.1f} Prozentpunkte")
print(f"China-Anteil t-1 ueber 25%: {(r.share_t1 > .25).mean():.2f}")
