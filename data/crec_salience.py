"""Salienz Chinas in Wirtschaftsdebatten des US-Kongresses 1995-2025 (Congressional Record, govinfo CREC).

Analog zu hansard_salience.py und hansard_competition.py. Laeuft nur auf dem Zwischenspeicher von
crec_fetch.py (data/raw/crec/).
Einheit: Granule (ein Abschnitt des Record mit eigenem Titel: Rede, Debatte, Einfuegung in Extensions).
Ausgeschlossen: Daily Digest und Front Matter.
Wirtschaftsdebatte: Titelfilter crec_econ_v1 (data/crec_filter.py).
Je Wirtschaftsdebatte: Woerter, Treffer China (ohne "Republic of China" = Taiwan), Japan, Mexiko;
China im Abstand von hoechstens 30 Woertern zu einem Wettbewerbswort.
Pruefstichprobe: je Jahr 10 zufaellige Sitzungstage vollstaendig; misst, welcher Anteil der Granules mit
China-Nennung einen Wirtschaftstitel hat (Trefferquote des Titelfilters).
Ergebnis: data/ds1_crec_granules.csv (Wirtschaftsdebatten), data/ds1_crec_salience.csv (Jahr),
data/ds1_crec_salience.txt (Perioden).

Aufruf aus dem Repo-Wurzelordner: python3 data/crec_salience.py
"""
import gzip
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import crec_fetch as F  # noqa: E402
from crec_filter import BENCH, COMP, FILTER_VERSION, TAIWAN, TARGET, TWORD, is_econ  # noqa: E402

C = D / "raw" / "crec"


def text(gid):
    p = C / "htm" / f"{gid}.htm.gz"
    if not p.exists():
        return None
    h = gzip.decompress(p.read_bytes()).decode("utf-8", errors="replace")
    h = re.sub(r"<[^>]+>", " ", h)
    h = re.sub(r"&[a-z]+;|&#\d+;", " ", h)
    return TAIWAN.sub(" ", h)


def measure(t):
    w = t.split()
    ws = [re.sub(r"[^\w'-]", "", x) for x in w]
    ti = [i for i, x in enumerate(ws) if TWORD.match(x)]
    ki = [i for i, x in enumerate(ws) if COMP.match(x)]
    near = bool(ti and ki) and any(abs(a - b) <= 30 for a in ti for b in ki)
    return {"words": len(w), "china_hits": len(TARGET.findall(t)), "china_competition": near,
            **{f"{k}_hits": len(rx.findall(t)) for k, rx in BENCH.items()}}


def wilson(k, n, z=1.96):
    if n == 0:
        return (np.nan, np.nan)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (100 * (c - h), 100 * (c + h))


def main():
    pk = {y: F.packages(y) for y in F.YEARS}
    samp = {x for v in F.sample_packages(pk).values() for x in v}
    rows = []
    for y, v in pk.items():
        for p in v:
            gp = C / "granules" / f"{p['packageId']}.json"
            for g in json.loads(gp.read_text()) if gp.exists() else []:
                if F.skip(g):
                    continue
                rows.append({"year": y, "date": g["dateIssued"], "package": p["packageId"], "granule": g["granuleId"],
                             "chamber": g["granuleClass"], "title": g["title"], "econ": is_econ(g["title"]),
                             "sample": p["packageId"] in samp})
    G = pd.DataFrame(rows)
    keep = G[G.econ | G["sample"]].copy()
    ms = []
    for gid in keep.granule:
        t = text(gid)
        ms.append(measure(t) if t is not None else {"words": np.nan})
    keep = pd.concat([keep.reset_index(drop=True), pd.DataFrame(ms)], axis=1)
    keep["loaded"] = keep.words.notna()
    keep["mentions_china"] = keep.china_hits > 0
    keep["filter"] = FILTER_VERSION
    E = keep[keep.econ]
    E.drop(columns=["sample"]).to_csv(D / "ds1_crec_granules.csv", index=False)

    S = keep[keep["sample"] & keep.loaded].copy()
    S["china_econ"] = S.mentions_china & S.econ
    S["china_competition"] = S.china_competition.fillna(False).astype(bool)
    S["china_comp_econ"] = S.china_competition & S.econ
    a = G.groupby("year").size().rename("granules_all")
    y = E[E.loaded].groupby("year").agg(econ_granules=("granule", "size"), econ_words=("words", "sum"),
                                        econ_china=("mentions_china", "sum"), econ_china_competition=("china_competition", "sum"),
                                        china_hits=("china_hits", "sum"), japan_hits=("japan_hits", "sum"),
                                        mexico_hits=("mexico_hits", "sum"))
    y = y.join(a).join(E.groupby("year").size().rename("econ_titles"))
    y = y.join(S.groupby("year").agg(sample_granules=("granule", "size"), sample_china=("mentions_china", "sum"),
                                     sample_china_econ=("china_econ", "sum"),
                                     sample_china_comp=("china_competition", "sum"),
                                     sample_china_comp_econ=("china_comp_econ", "sum")))
    y["salience_share"] = (y.econ_china / y.econ_granules).round(4)
    y["competition_share"] = (y.econ_china_competition / y.econ_granules).round(4)
    for k in ("china", "japan", "mexico"):
        y[f"{k}_hits_per_100k_words"] = (1e5 * y[f"{k}_hits"] / y.econ_words).round(2)
    y["sample_filter_recall"] = (y.sample_china_econ / y.sample_china).round(3)
    y["sample_filter_recall_comp"] = (y.sample_china_comp_econ / y.sample_china_comp).round(3)
    y = y.reset_index()
    y.to_csv(D / "ds1_crec_salience.csv", index=False)

    out = [f"Filter {FILTER_VERSION}; Granules ohne Daily Digest und Front Matter: {len(G)}; "
           f"mit Wirtschaftstitel: {int(G.econ.sum())}; davon Volltext geladen: {int(E.loaded.sum())}"]
    per = pd.cut(E.year, [1994, 2000, 2009, 2017, 2025], labels=["1995-2000", "2001-2009", "2010-2017", "2018-2025"])
    out.append("Periode | Wirtschaftsdebatten | mit China % [95%] | China nahe Wettbewerbswort % [95%] | China/Japan/Mexiko je 100.000 Woerter")
    for lab, z in E[E.loaded].groupby(per[E.loaded], observed=True):
        n, k, c = len(z), int(z.mentions_china.sum()), int(z.china_competition.sum())
        lo, hi = wilson(k, n)
        clo, chi = wilson(c, n)
        wsum = z.words.sum()
        out.append(f"{lab} | {n} | {100*k/n:.1f} [{lo:.1f}-{hi:.1f}] | {100*c/n:.1f} [{clo:.1f}-{chi:.1f}] | "
                   f"{1e5*z.china_hits.sum()/wsum:.1f} / {1e5*z.japan_hits.sum()/wsum:.1f} / {1e5*z.mexico_hits.sum()/wsum:.1f}")
    s = S
    k = int(s.mentions_china.sum())
    ke = int((s.mentions_china & s.econ).sum())
    out.append(f"Pruefstichprobe: {s.package.nunique()} Sitzungstage, {len(s)} Granules, davon {k} mit China-Nennung; "
               f"{ke} davon mit Wirtschaftstitel ({100*ke/max(k,1):.0f} %). China-Treffer in der Stichprobe: "
               f"{int(s.china_hits.sum())}, davon in Wirtschaftsdebatten {int(s[s.econ].china_hits.sum())} "
               f"({100*s[s.econ].china_hits.sum()/max(s.china_hits.sum(),1):.0f} %)")
    kc = int(s.china_competition.sum())
    kce = int((s.china_competition & s.econ).sum())
    out.append(f"Pruefstichprobe, China nahe Wettbewerbswort (wirtschaftliche China-Nennung): {kc} Granules, davon "
               f"{kce} mit Wirtschaftstitel ({100*kce/max(kc,1):.0f} %)")
    nc = s[s.china_competition & ~s.econ]
    out.append("Haeufigste Titel verfehlter Granules mit China nahe Wettbewerbswort: " +
               "; ".join(nc.title.str.upper().str[:50].value_counts().head(12).index))
    nc = s[s.mentions_china & ~s.econ]
    out.append("Haeufigste Titel der verfehlten China-Granules: " +
               "; ".join(nc.title.str.upper().str[:50].value_counts().head(12).index))
    (D / "ds1_crec_salience.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
