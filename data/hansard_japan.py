"""Aufmerksamkeit fuer Japan in britischen Wirtschaftsdebatten 1920-1939 (Historic Hansard), Gegenstueck zu
hansard_salience.py (Deutschland 1850-1914). Gleicher Titelfilter (ECON), gleiche Abruf- und Cache-Logik.

Je Wirtschaftsdebatte: Nennungen Japans (japan, japanese), Nennungen von Baumwolle/Textil/Lancashire und
Gemeinsamnennung. Je Jahr: Anteil der Wirtschaftsdebatten mit Japan, Treffer je 100.000 Woerter, Anteil mit
Japan und Baumwolle zugleich.
Ergebnis: data/ds1_hansard_japan.csv (Jahr), data/ds1_hansard_japan_sections.csv (Debatte).
Aufruf aus dem Repo-Wurzelordner: python3 data/hansard_japan.py [erstes_jahr] [letztes_jahr]
"""
import concurrent.futures as cf
import re
import sys

import pandas as pd

sys.path.insert(0, __import__("os").path.dirname(__file__))
from hansard_salience import D, ECON, days, get, sections, text_of  # noqa: E402

TARGET = re.compile(r"\b(japan|japanese)\b", re.I)
COTTON = re.compile(r"\b(cotton|textiles?|piece[- ]goods|lancashire|rayon)\b", re.I)


def run(y0, y1):
    with cf.ThreadPoolExecutor(4) as ex:
        dl = {y: ex.submit(days, y) for y in range(y0, y1 + 1)}
        jobs = [ex.submit(sections, y, d) for y in dl for d in dl[y].result()]
        secs = pd.DataFrame([r for j in jobs for r in j.result()]).drop_duplicates("url")
    secs["econ"] = secs.title.str.lower().apply(lambda s: any(k in s for k in ECON))
    econ = secs[secs.econ].copy()
    with cf.ThreadPoolExecutor(4) as ex:
        texts = [text_of(h) for h in ex.map(lambda u: get(u) or "", econ.url)]
    econ["words"] = [len(t.split()) for t in texts]
    econ["japan_hits"] = [len(TARGET.findall(t)) for t in texts]
    econ["cotton_hits"] = [len(COTTON.findall(t)) for t in texts]
    econ["fetched"] = [bool(t.strip()) for t in texts]
    econ["japan"] = econ.japan_hits > 0
    econ["japan_cotton"] = econ.japan & (econ.cotton_hits > 0)
    econ.to_csv(D / "ds1_hansard_japan_sections.csv", index=False)
    yr = secs.groupby("year").size().rename("all_sections").to_frame()
    g = econ.groupby("year")
    yr["econ_sections"] = g.size()
    yr["econ_mentioning_japan"] = g.japan.sum()
    yr["salience_share"] = (yr.econ_mentioning_japan / yr.econ_sections).round(4)
    yr["japan_hits_per_100k_words"] = (g.japan_hits.sum() / g.words.sum() * 1e5).round(2)
    yr["econ_japan_cotton"] = g.japan_cotton.sum()
    yr["japan_cotton_share"] = (yr.econ_japan_cotton / yr.econ_sections).round(4)
    yr["not_fetched"] = g.fetched.apply(lambda s: int((~s).sum()))
    yr.reset_index().to_csv(D / "ds1_hansard_japan.csv", index=False)
    print(yr.to_string())


if __name__ == "__main__":
    a = [int(x) for x in sys.argv[1:3]] or [1920, 1939]
    run(a[0], a[-1])
