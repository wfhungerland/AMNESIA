"""Section-301-Zoelle gegen China je HTS8-Position: Liste, Inkrafttreten, Satz; Ueberpruefung 2024.

Quelle: Federal Register ueber govinfo (Collection FR), amtliche Fassung der USTR-Bekanntmachungen:
  Liste 1: 83 FR 28710, FR Doc. 2018-13248 (20.6.2018), Annex A; Zoll 25 % ab 6.7.2018
  Liste 2: 83 FR 40823, FR Doc. 2018-17709 (16.8.2018), Annex A; 25 % ab 23.8.2018
  Liste 3: 83 FR 47974, FR Doc. 2018-20610 (21.9.2018), Annex A; 10 % ab 24.9.2018 (spaeter 25 %)
  Liste 4A und 4B: 84 FR 43304, FR Doc. 2019-17865 (20.8.2019), Annex A, U.S. note 20(s) (4A, Heading
    9903.88.15) und Heading 9903.88.16 (4B); 10 % ab 1.9.2019 (4A) bzw. 15.12.2019 (4B, spaeter ausgesetzt)
  Ueberpruefung 2024: 89 FR 76581, FR Doc. 2024-21217 (18.9.2024), Annex A, Tabelle der Erhoehungen nach Produktgruppe
Fundstellen, Saetze und Daten am 22.11.2026 an den Texten in data/raw/fr/ geprueft (erste Seite, "additional
NN percent ad valorem", Datum des Inkrafttretens). Spaetere Aenderungen der Saetze (Liste 3 auf 25 %, 4A auf
7,5 %) stehen in anderen Bekanntmachungen und werden hier nicht verwendet.
Die Anhaenge der Listen 1 bis 4 stehen nur in der PDF-Fassung (Textschicht, pdftotext -layout).

Ergebnis: data/ds1_301_hts8.csv (Position x Liste), data/ds1_301_hs4.csv (HS4: Anteil der Positionen je Liste,
Erhoehung 2024). Aufruf aus dem Repo-Wurzelordner: python3 data/fr301_lists.py
"""
import os
import re
import subprocess
import urllib.request
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
C = D / "raw" / "fr"
C.mkdir(parents=True, exist_ok=True)
API = "https://api.govinfo.gov/packages"
DOCS = {"2018-13248": "2018-06-20", "2018-17709": "2018-08-16", "2018-20610": "2018-09-21",
        "2019-17865": "2019-08-20", "2024-21217": "2024-09-18"}
R8 = re.compile(r"\b(\d{4}\.\d{2}\.\d{2})\b")


def fetch(doc, kind):
    f = C / f"{doc}.{ 'pdf' if kind == 'pdf' else 'htm'}"
    if not f.exists():
        url = f"{API}/FR-{DOCS[doc]}/granules/{doc}/{kind}"
        req = urllib.request.Request(url, headers={"X-Api-Key": os.environ.get("GOVINFO_KEY", "DUMMY"), "User-Agent": "research-client/1.0"})
        f.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    return f


def lines(doc):
    t = C / f"{doc}.txt"
    if not t.exists():
        subprocess.run(["pdftotext", "-layout", str(fetch(doc, "pdf")), str(t)], check=True)
    return t.read_text(errors="replace").split("\n")


def codes(L, a, b):
    return sorted({c for l in L[a:b] for c in R8.findall(l) if not c.startswith("99")})


def first(L, pat, start=0):
    rx = re.compile(pat)
    return next(i for i, l in enumerate(L) if i >= start and rx.search(l))


rows = []
# Annex A endet jeweils mit der Ueberschrift ANNEX B (Warenbeschreibungen).
for doc, lab, date, rate in [("2018-13248", "1", "2018-07-06", 25), ("2018-17709", "2", "2018-08-23", 25),
                             ("2018-20610", "3", "2018-09-24", 10)]:
    L = lines(doc)
    for c in codes(L, 0, first(L, r"^\s+ANNEX B\s*$")):
        rows.append({"hts8": c, "list": lab, "effective": date, "rate_initial": rate})
L = lines("2019-17865")
a4 = first(L, r'"\(s\) Heading 9903\.88\.15 applies to')
b4 = first(L, r"^\s+ANNEX B\s*$")
a4b = first(L, r"Products of China that are provided for in heading 9903\.88\.16")
b4b = first(L, r"^\s+ANNEX D\s*$")
for c in codes(L, a4, b4):
    rows.append({"hts8": c, "list": "4A", "effective": "2019-09-01", "rate_initial": 10})
for c in codes(L, a4b, b4b):
    rows.append({"hts8": c, "list": "4B", "effective": "2019-12-15", "rate_initial": 10})
H = pd.DataFrame(rows)

# Ueberpruefung 2024, Annex A: "Code....  Beschreibung   Satz   Jahr"
t = re.sub(r"</?[A-Za-z][^>]*>", "", fetch("2024-21217", "htm").read_text(errors="replace")).split("\n")
a, b = first(t, r"^Annex A--Tariff Increases"), first(t, r"^Annex B--Exclusions")
inc = []
group = None
seg = t[a:b]
for j, l in enumerate(seg):
    if 0 < j < len(seg) - 1 and seg[j - 1].startswith("---") and seg[j + 1].startswith("---") \
            and l.strip() and not R8.search(l) and "HTSUS" not in l:
        group = l.strip()
        continue
    m = re.match(r"^(\d{4}\.\d{2}\.\d{2}(?:\d{2})?)\.{2,}.*?\s(\d{2,3})\s+(\d{4})\s*$", l)
    if m:
        inc.append({"hts": m.group(1), "hts8": m.group(1)[:10], "rate_2024": int(m.group(2)), "year_2024": int(m.group(3)), "group_2024": group})
I = pd.DataFrame(inc).drop_duplicates("hts")
H.to_csv(D / "ds1_301_hts8.csv", index=False)
I.to_csv(D / "ds1_301_review2024.csv", index=False)

H["hs4"] = H.hts8.str[:4]
P = H.pivot_table(index="hs4", columns="list", values="hts8", aggfunc="count", fill_value=0)
P["lines"] = P.sum(axis=1)
for k in ["1", "2", "3", "4A", "4B"]:
    P[f"share_{k}"] = (P.get(k, 0) / P.lines).round(3)
P["share_12"] = (P.share_1 + P.share_2).round(3)
I["hs4"] = I.hts8.str[:4]
P = P.join(I.groupby("hs4").agg(lines_2024=("hts", "size"), rate_2024_max=("rate_2024", "max")), how="outer")
P["lines"] = P.lines.fillna(0).astype(int)
P["review2024"] = P.lines_2024.notna()
P.reset_index().to_csv(D / "ds1_301_hs4.csv", index=False)
print(H.groupby("list").size().to_string())
print("Ueberpruefung 2024: Positionen", len(I), "; Gruppen", I.group_2024.nunique(), "; HS4", I.hs4.nunique())
print(I.group_2024.value_counts().to_string())
