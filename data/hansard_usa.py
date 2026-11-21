"""Vergleich: Nennung der USA in denselben britischen Wirtschaftsdebatten 1850-1914 (nur Zwischenspeicher).

Gleiche Debatten und Masse wie fuer Deutschland, damit beide Reihen vergleichbar sind.
Ergebnis: data/ds1_hansard_usa.csv
"""
import hashlib, re
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
C = D / "raw" / "hansard"
US = re.compile(r"\b(america|american|americans|united states)\b", re.I)
K = re.compile(r"\b(competition|competitor|competitors|compete|competing|dumping|dumped|unfair|bount\w*|subsid\w*|undersell\w*|cheap|cheaper|imitat\w*|rival\w*)\b", re.I)


def text(url):
    f = C / (hashlib.sha1(url.encode()).hexdigest() + ".html")
    h = f.read_text(errors="replace") if f.exists() else ""
    h = re.sub(r"(?s)<(script|style|head).*?</\1>", " ", h)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h))


s = pd.read_csv(D / "ds1_hansard_sections.csv")
hits, comp = [], []
for u in s.url:
    t = text(u)
    w = t.split()
    ui = [i for i, x in enumerate(w) if US.search(x) or (x.lower().startswith("states") and i and w[i - 1].lower() == "united")]
    ki = [i for i, x in enumerate(w) if K.search(x)]
    hits.append(len(US.findall(t)))
    comp.append(any(abs(a - b) <= 30 for a in ui for b in ki))
s["us_hits"], s["us_competition"] = hits, comp
s["us_mention"] = s.us_hits > 0
g = s.groupby("year").agg(econ_sections=("url", "size"), us_mention=("us_mention", "sum"), us_competition=("us_competition", "sum"),
                          us_hits=("us_hits", "sum"), de_hits=("target_hits", "sum"), words=("words", "sum"),
                          de_mention=("mentions_target", "sum"), de_competition=("germany_competition", "sum"))
g["us_per_100k"] = (g.us_hits / g.words * 1e5).round(2)
g["de_per_100k"] = (g.de_hits / g.words * 1e5).round(2)
g.reset_index().to_csv(D / "ds1_hansard_usa.csv", index=False)
g["p"] = pd.cut(g.index, [1849, 1869, 1892, 1902, 1914], labels=["1850-69", "1870-92", "1893-1902", "1903-14"])
p = g.groupby("p", observed=True)[["econ_sections", "us_mention", "us_competition", "de_mention", "de_competition", "us_hits", "de_hits", "words"]].sum()
out = pd.DataFrame({"USA_nennung_%": 100 * p.us_mention / p.econ_sections, "USA_wettb_%": 100 * p.us_competition / p.econ_sections,
                    "USA_je100k": p.us_hits / p.words * 1e5, "DE_nennung_%": 100 * p.de_mention / p.econ_sections,
                    "DE_wettb_%": 100 * p.de_competition / p.econ_sections, "DE_je100k": p.de_hits / p.words * 1e5}).round(2)
print(out.to_string())
