"""Feste Wendungen in britischen Wirtschaftsdebatten 1850-1914 (nur Zwischenspeicher):
'American competition', 'American invasion' gegen 'German competition', 'Made in Germany'.
Ergebnis: data/ds1_hansard_phrases.csv (Debatten je Jahr mit der Wendung)."""
import hashlib, re
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
C = D / "raw" / "hansard"
P = {"american_competition": r"american\s+competition", "american_invasion": r"american\s+invasion",
     "german_competition": r"german\s+competition", "made_in_germany": r"made\s+in\s+germany"}
P = {k: re.compile(v, re.I) for k, v in P.items()}
s = pd.read_csv(D / "ds1_hansard_sections.csv")
rows = []
for _, r in s.iterrows():
    f = C / (hashlib.sha1(r.url.encode()).hexdigest() + ".html")
    t = re.sub(r"<[^>]+>", " ", f.read_text(errors="replace")) if f.exists() else ""
    rows.append({"year": r.year, **{k: bool(rx.search(t)) for k, rx in P.items()}})
d = pd.DataFrame(rows).groupby("year").sum().reset_index()
d.to_csv(D / "ds1_hansard_phrases.csv", index=False)
d["p"] = pd.cut(d.year, [1849, 1869, 1892, 1902, 1914], labels=["1850-69", "1870-92", "1893-1902", "1903-14"])
print(d.groupby("p", observed=True)[list(P)].sum().to_string())
print(d[(d.year >= 1898) & (d.year <= 1906)].to_string(index=False))
