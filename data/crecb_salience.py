"""Japan (und China) im US-Kongress auf Basis von Stichprobentagen: gebundener Record 1955-1994 (CRECB) und
Prueftage des taeglichen Record 1995-2025 (CREC, je Jahr 10 Tage vollstaendig).

Laeuft nur auf den Zwischenspeichern von crecb_fetch.py und crec_fetch.py. Ohne Debattentitel gibt es
keinen Wirtschaftsfilter: gemessen wird im gesamten Text der Stichprobentage.
Je Jahr: Woerter, Nennungen Japan, China, Deutschland je 100.000 Woerter; Japan (China) im Abstand von
hoechstens 30 Woertern zu einem Wettbewerbswort; je Sektor (crec_filter.JP_FINE) die Zahl der Stellen, an
denen Japan hoechstens 30 Woerter von einem Sektorwort steht, je 1 Mio. Woerter.

Test (Japan): Aufmerksamkeit fuer Japan im Sektor in den 5 Jahren vor gegen ab der Kreuzung (SITC Rev. 1,
data/population_crossovers.csv); Sektoren mit breiter Massnahme gegen Japan (data/broad_register.csv) gegen
verdraengte Sektoren ohne; Bruchtest wie tests_sequence.py.
Ergebnis: data/ds1_crecb_years.csv, data/ds1_crecb_sector_years.csv, data/ds1_crecb_test.csv,
data/ds1_crecb_test.txt. Aufruf: python3 data/crecb_salience.py
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
import crecb_fetch as B  # noqa: E402
from crec_filter import COMP, CWORD, GWORD, JP_FINE, JP_FINE_RX, JWORD, TAIWAN, jp_fine_of  # noqa: E402
from crec_stats import perm_p  # noqa: E402

JOIN = [(re.compile(r"\bmachine\s+tools?\b", re.I), "machine-tools"), (re.compile(r"\bball\s+bearings\b", re.I), "ball-bearings")]


def tokens(t):
    t = TAIWAN.sub(" ", t)
    t = re.sub(r"-\s*\n\s*", "", t)  # Silbentrennung am Zeilenende im gebundenen Record
    for rx, rep in JOIN:
        t = rx.sub(rep, t)
    return [re.sub(r"[^\w'-]", "", x) for x in t.split()]


def near(a, b, k=30):
    if not a or not b:
        return 0
    b = np.asarray(b)
    return int(sum(np.any(np.abs(b - x) <= k) for x in a))


def day_measure(w):
    ji = [i for i, x in enumerate(w) if JWORD.match(x)]
    ci = [i for i, x in enumerate(w) if CWORD.match(x)]
    gi = [i for i, x in enumerate(w) if GWORD.match(x)]
    ki = [i for i, x in enumerate(w) if COMP.match(x)]
    r = {"words": len(w), "japan": len(ji), "china": len(ci), "germany": len(gi),
         "japan_comp": near(ji, ki), "china_comp": near(ci, ki)}
    for k, rx in JP_FINE_RX.items():
        si = [i for i, x in enumerate(w) if rx.match(x)]
        r[f"s_{k}"] = len(si)
        r[f"j_{k}"] = near(ji, si)
    return r


def docs():
    for y in range(1955, 1995):  
        lp = B.C / "lists" / f"{y}.json"
        if not lp.exists():
            continue
        for d, gs in B.sample(y).items():
            ts = [B.txt_path(g) for _, g, _ in gs]
            if all(p.exists() for p in ts):
                yield y, d, "CRECB", " ".join(gzip.decompress(p.read_bytes()).decode("utf-8", "replace") for p in ts)
    pk = {y: F.packages(y) for y in F.YEARS}
    for y, v in F.sample_packages(pk).items():
        for pid in v:
            gp = F.C / "granules" / f"{pid}.json"
            if not gp.exists():
                continue
            parts = []
            for g in json.loads(gp.read_text()):
                p = F.htm_path(g["granuleId"])
                if not F.skip(g) and p.exists():
                    parts.append(re.sub(r"<[^>]+>", " ", gzip.decompress(p.read_bytes()).decode("utf-8", "replace")))
            if parts:
                yield y, pid, "CREC", " ".join(parts)


def main():
    rows = [{"year": y, "day": d, "source": s, **day_measure(tokens(t))} for y, d, s, t in docs()]
    X = pd.DataFrame(rows)
    Y = X.groupby(["year", "source"]).agg(days=("day", "size"), **{c: (c, "sum") for c in X.columns if c not in ("year", "day", "source")}).reset_index()
    for c in ("japan", "china", "germany"):
        Y[f"{c}_per_100k"] = (1e5 * Y[c] / Y.words).round(2)
    for c in ("japan_comp", "china_comp"):
        Y[f"{c}_per_1m"] = (1e6 * Y[c] / Y.words).round(2)
    Y[["year", "source", "days", "words", "japan", "china", "germany", "japan_per_100k", "china_per_100k",
       "germany_per_100k", "japan_comp_per_1m", "china_comp_per_1m"]].to_csv(D / "ds1_crecb_years.csv", index=False)
    SY = Y.melt(id_vars=["year", "words"], value_vars=[f"j_{k}" for k in JP_FINE], var_name="sector", value_name="japan_near")
    SY["sector"] = SY.sector.str[2:]
    SY["per_1m"] = (1e6 * SY.japan_near / SY.words).round(3)
    SY.to_csv(D / "ds1_crecb_sector_years.csv", index=False)

    cr = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
    cr = cr[(cr.challenger == "JP") & (cr.data == "s1")].copy()
    cr["sector"] = cr.code.map(jp_fine_of)
    reg = pd.read_csv(D / "broad_register.csv", dtype=str)
    reg = reg[reg.target.str.contains("JP")]
    T = []
    for k in JP_FINE:
        z = cr[cr.sector == k]
        cy = int(z.crossover_year.min()) if len(z) else None
        cens = bool(len(z)) and bool(z[z.crossover_year == cy].left_censored.any())
        ms = sorted((int(r.year), r.instrument_id) for _, r in reg.iterrows()
                    if any(jp_fine_of(c) == k for c in str(r.codes_s1).split(";")))
        s = SY[SY.sector == k].set_index("year")
        rec = {"sector": k, "crossover_year": cy, "crossover_censored": cens, "measure": bool(ms),
               "measure_first_year": ms[0][0] if ms else None, "measure_ids": ";".join(i for _, i in ms)}
        if cy is not None:
            pre = s[(s.index >= cy - 5) & (s.index <= cy - 1)]
            post = s[(s.index >= cy) & (s.index <= cy + 4)]
            rec["voice_pre"] = round(1e6 * pre.japan_near.sum() / pre.words.sum(), 2) if len(pre) >= 3 else np.nan
            rec["voice_post"] = round(1e6 * post.japan_near.sum() / post.words.sum(), 2) if len(post) else np.nan
        w0 = s[(s.index >= 1960) & (s.index <= 1975)]
        rec["voice_1960_1975"] = round(1e6 * w0.japan_near.sum() / w0.words.sum(), 2) if len(w0) else np.nan
        if ms:
            mw = s[(s.index >= ms[0][0] - 5) & (s.index <= ms[0][0] - 1)]
            rec["voice_5y_before_measure"] = round(1e6 * mw.japan_near.sum() / mw.words.sum(), 2) if len(mw) else np.nan
        T.append(rec)
    T = pd.DataFrame(T)
    T.to_csv(D / "ds1_crecb_test.csv", index=False)
    out = [f"Stichprobentage: CRECB {int((X.source=='CRECB').sum())} ({X[X.source=='CRECB'].year.min()}-{X[X.source=='CRECB'].year.max()}), "
           f"CREC {int((X.source=='CREC').sum())}; Woerter {int(X.words.sum()):,}"]
    per = pd.cut(Y.year, [1954, 1964, 1974, 1984, 1994, 2004, 2014, 2025])
    P = Y.groupby(per, observed=True)[["words", "japan", "china", "japan_comp", "china_comp"]].sum()
    out.append("Periode | Japan je 100.000 W. | China je 100.000 W. | Japan nahe Wettbewerb je 1 Mio. | China nahe Wettbewerb je 1 Mio.")
    for i, r in P.iterrows():
        out.append(f"{i} | {1e5*r.japan/r.words:.1f} | {1e5*r.china/r.words:.1f} | {1e6*r.japan_comp/r.words:.2f} | {1e6*r.china_comp/r.words:.2f}")
    out.append(T.to_string(index=False))
    A = T[(~T.crossover_censored) & T.voice_pre.notna()]
    out.append(f"Zeitfolge Japan: voice nach > vor in {(A.voice_post > A.voice_pre).sum()} von {len(A)} Sektoren")
    for col in ["voice_1960_1975", "voice_pre", "voice_post"]:
        obs, p, k, n0 = perm_p(T[col], T.measure)
        out.append(f"Auswahl Japan {col}: mit Massnahme {T[T.measure][col].mean():.2f} (n={k}), ohne {T[~T.measure][col].mean():.2f} "
                   f"(n={n0}); Differenz {obs:+.2f}, p = {p:.3f}")
    (D / "ds1_crecb_test.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
