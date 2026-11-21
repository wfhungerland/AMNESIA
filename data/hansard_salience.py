"""Salienz Deutschlands in britischen Wirtschaftsdebatten 1850-1914 (Historic Hansard).

Schritt 1: alle Sitzungstage je Jahr und alle Debattentitel (Commons und Lords).
Schritt 2: Wirtschaftsdebatten per festem Titel-Stichwortfilter (ECON, unten).
Schritt 3: Volltext dieser Debatten laden und Nennung des Ziellands pruefen (TARGET).
Ergebnis: data/ds1_hansard_salience.csv (Jahr), data/ds1_hansard_sections.csv (Debatte).
Rohseiten werden in data/raw/hansard/ zwischengespeichert, damit Wiederholungen nichts neu laden.

Aufruf aus dem Repo-Wurzelordner: python3 data/hansard_salience.py [erstes_jahr] [letztes_jahr]
"""
import concurrent.futures as cf
import hashlib
import re
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

BASE = "https://api.parliament.uk"
D = Path(__file__).resolve().parent
CACHE = D / "raw" / "hansard"
CACHE.mkdir(parents=True, exist_ok=True)
MONTHS = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
FILTER_VERSION = "econ_v1"

# Wirtschaftsdebatte, wenn der Titel einen dieser Wortstaemme enthaelt (Kleinschreibung).
ECON = ["trade", "tariff", "commerc", "import", "export", "duty", "duties", "customs", "manufactur",
        "industr", "merchandise", "bount", "shipping", "navigation", "patent", "depression",
        "dumping", "free trade", "fair trade", "protection", "sugar", "iron", "steel", "coal",
        "cotton", "woollen", "textile", "chemical", "dye", "cutlery", "competition", "fiscal",
        "preference", "most favoured", "treaty", "consular"]
# Nennung des Ziellands im Volltext. Vor 1871 auch Preussen und Zollverein.
TARGET = re.compile(r"\b(german|germany|germans|prussia|prussian|zollverein)\b", re.I)


def get(url, tries=4):
    f = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".html")
    if f.exists():
        return f.read_text(encoding="utf-8", errors="replace")
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "research-client/1.0"})
            with urllib.request.urlopen(req, timeout=30) as r:
                t = r.read().decode("utf-8", errors="replace")
            f.write_text(t, encoding="utf-8")
            time.sleep(0.2)
            return t
        except urllib.error.HTTPError as e:
            if e.code == 404:
                f.write_text("", encoding="utf-8")
                return ""
            time.sleep(2 ** i)
        except Exception:
            time.sleep(2 ** i)
    return None


def days(year):
    out = []
    for m in MONTHS:
        t = get(f"{BASE}/historic-hansard/sittings/{year}/{m}/")
        if t:
            ds = sorted(set(re.findall(rf'href="/historic-hansard/sittings/{year}/{m}/(\d+)"', t)), key=int)
            out += [f"{m}/{d}" for d in ds]
    return out


def sections(year, day):
    t = get(f"{BASE}/historic-hansard/sittings/{year}/{day}")
    if not t:
        return []
    rows = []
    for house, path, title in re.findall(
            rf'<a href="/historic-hansard/(commons|lords)/({year}/{day}/[^"#]+)">([^<]+)</a>', t):
        rows.append({"year": year, "date": f"{year}/{day}", "house": house,
                     "url": f"{BASE}/historic-hansard/{house}/{path}", "title": title.strip()})
    return rows


def text_of(html):
    html = re.sub(r"(?s)<(script|style|head).*?</\1>", " ", html)
    body = re.sub(r"<[^>]+>", " ", html)
    return re.sub(r"\s+", " ", body)


def run(y0, y1):
    with cf.ThreadPoolExecutor(4) as ex:
        dl = {y: ex.submit(days, y) for y in range(y0, y1 + 1)}
        jobs = [ex.submit(sections, y, d) for y in dl for d in dl[y].result()]
        secs = pd.DataFrame([r for j in jobs for r in j.result()]).drop_duplicates("url")
    secs["econ"] = secs.title.str.lower().apply(lambda s: any(k in s for k in ECON))
    econ = secs[secs.econ].copy()
    with cf.ThreadPoolExecutor(4) as ex:
        texts = list(ex.map(lambda u: get(u) or "", econ.url))
    econ["words"] = [len(text_of(h).split()) for h in texts]
    econ["target_hits"] = [len(TARGET.findall(text_of(h))) for h in texts]
    econ["mentions_target"] = econ.target_hits > 0
    econ["fetched"] = [bool(h) for h in texts]
    econ["filter_version"] = FILTER_VERSION
    econ.to_csv(D / "ds1_hansard_sections.csv", index=False)
    yr = secs.groupby("year").size().rename("all_sections").to_frame()
    g = econ.groupby("year")
    yr["econ_sections"] = g.size()
    yr["econ_mentioning_germany"] = g.mentions_target.sum()
    yr["salience_share"] = (yr.econ_mentioning_germany / yr.econ_sections).round(4)
    yr["germany_hits_per_100k_words"] = (g.target_hits.sum() / g.words.sum() * 1e5).round(2)
    yr["filter_version"] = FILTER_VERSION
    yr.reset_index().to_csv(D / "ds1_hansard_salience.csv", index=False)
    print(yr.to_string())


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:3]] or [1850, 1914]
    run(a[0], a[-1])
