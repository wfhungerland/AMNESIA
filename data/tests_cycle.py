"""Konjunkturkontrolle (Panel-Revision): Fallen Reaktionen in Abschwuenge des Etablierten?

Produktionsluecke = Abweichung von log(BIP) vom HP-Trend (lambda 100, jaehrlich), BIP = BIP pro Kopf mal
Bevoelkerung aus Maddison 2023. Etablierter: GB (Fall DE), USA (JP, KR ausser Schiffbau, CN), Japan
(Schiffbau), EU durch Deutschland angenaehert. Vergleich: Anteil der Reaktionsjahre mit negativer Luecke
gegen den Anteil aller Jahre mit negativer Luecke im Fallfenster. Ergebnis: data/tests_cycle.txt
"""
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
m = pd.read_stata(D / "raw" / "maddison2023_web.dta")
gaps = {}
for c in ["GBR", "USA", "JPN", "DEU"]:
    x = m[(m.countrycode == c) & (m.year >= 1820)].dropna(subset=["gdppc", "pop"]).sort_values("year")
    x = x[x.year >= 1950] if c == "JPN" else x  # Japan vor 1950 lueckenhaft
    y = np.log(x["gdppc"].values * x["pop"].values)
    n = len(y); lam = 100.0
    Dm = np.zeros((n - 2, n))
    for i in range(n - 2):
        Dm[i, i:i + 3] = [1, -2, 1]
    trend = np.linalg.solve(np.eye(n) + lam * Dm.T @ Dm, y)
    gaps[c] = pd.Series(y - trend, index=x.year.astype(int).values)
e = pd.read_csv(D / "ds1_events.csv")
e["binding"] = e.type.str.startswith("binding") | (e.type == "denial")
inc = {"GB": "GBR", "GB+FR": "GBR", "US": "USA", "JP": "JPN", "EU": "DEU"}
e["inc_iso"] = e.incumbent.map(inc)
e["gap"] = [gaps[i].get(y, np.nan) for i, y in zip(e.inc_iso, e.year)]
window = {"DE": (1850, 1914), "JP": (1950, 1990), "KR": (1980, 2020), "CN": (2000, 2024)}
out = []
for label, sub in [("alle", e), ("bindend", e[e.binding])]:
    s = sub.dropna(subset=["gap"])
    base = []
    for _, r in s.iterrows():
        a, b = window[r.case]
        g = gaps[r.inc_iso].loc[a:b]
        base.append((g < 0).mean())
    out.append(f"{label}: {len(s)} Reaktionen mit Luecke; Anteil in Jahren negativer Luecke {np.mean(s.gap < 0):.2f}; "
               f"erwartet bei Zufall {np.mean(base):.2f}; mittlere Luecke {s.gap.mean():+.3f}")
    for ph in ["absorption", "post"]:
        z = s[s.phase == ph]
        if len(z):
            out.append(f"   {ph}: n={len(z)}, Anteil negative Luecke {np.mean(z.gap < 0):.2f}")
e[["response_id", "incumbent", "year", "gap"]].to_csv(D / "tests_cycle_events.csv", index=False)
(D / "tests_cycle.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
