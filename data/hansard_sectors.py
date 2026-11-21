"""Sektorale Aufschluesselung der Hansard-Auswertung (laeuft nur auf dem Zwischenspeicher).

Je Wirtschaftsdebatte: Erwaehnt sie einen Sektor (mind. 3 Sektorwoerter)? Steht Deutschland
im Abstand von hoechstens 30 Woertern zu einem Sektorwort? Ergebnis: data/ds1_hansard_sectors.csv
"""
import hashlib, re
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
C = D / "raw" / "hansard"
T = re.compile(r"^(german|germany|germans|prussia|prussian|zollverein)$", re.I)
SECT = {
    "iron_steel": r"^(iron|steel|pig-iron|ironworks|bessemer|rails)$",
    "chem_dyes": r"^(dye|dyes|dyestuffs?|aniline|alizarin|indigo|chemical|chemicals|coal-tar)$",
    "sugar": r"^(sugar|sugars|beet|bounty|bounties)$",
    "textiles": r"^(cotton|woollen|wool|textile|textiles|linen|silk)$",
}
SECT = {k: re.compile(v, re.I) for k, v in SECT.items()}


def words(url):
    f = C / (hashlib.sha1(url.encode()).hexdigest() + ".html")
    h = f.read_text(errors="replace") if f.exists() else ""
    h = re.sub(r"(?s)<(script|style|head).*?</\1>", " ", h)
    w = re.sub(r"<[^>]+>", " ", h).split()
    return [re.sub(r"[^\w-]", "", x) for x in w]


s = pd.read_csv(D / "ds1_hansard_sections.csv")
rows = []
for _, r in s.iterrows():
    w = words(r.url)
    ti = [i for i, x in enumerate(w) if T.match(x)]
    for k, rx in SECT.items():
        si = [i for i, x in enumerate(w) if rx.match(x)]
        if len(si) >= 3:
            near = any(abs(a - b) <= 30 for a in ti for b in si)
            rows.append({"year": r.year, "url": r.url, "sector": k, "sector_words": len(si), "germany_near": near})
out = pd.DataFrame(rows)
out.to_csv(D / "ds1_hansard_sectors.csv", index=False)
out["p"] = pd.cut(out.year, [1849, 1869, 1892, 1902, 1914], labels=["1850-69", "1870-92", "1893-1902", "1903-14"])
t = out.groupby(["sector", "p"], observed=True).agg(debates=("url", "size"), with_germany=("germany_near", "sum"))
t["share_%"] = (100 * t.with_germany / t.debates).round(1)
print(t.to_string())
