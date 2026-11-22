"""Sektorgroesse bereinigt: Anteil der Sektorwort-Nennungen mit Japan bzw. Korea im Umkreis von 30 Woertern.

Der gebundene Record hat keine Debattentitel; Debatten lassen sich nicht abgrenzen. Statt "Sektordebatten mit
dem Aufsteiger" zaehlt das Skript daher je Sektor alle Nennungen eines Sektorworts auf den Stichprobentagen
(Nenner, misst, wie viel ueber den Sektor gesprochen wird) und davon jene, bei denen Japan (Korea) hoechstens
30 Woerter entfernt steht (Zaehler). Der Anteil ist unabhaengig davon, wie gross oder wie oft debattiert ein
Sektor ist. Gleiche Tage, Woerter und Sektoren wie crecb_salience.py (Japan) und crecb_korea.py (Korea).
Zusaetzlich das Sektorvolumen selbst (Nennungen der Sektorwoerter je 1 Mio. Woerter), vor und ab der Kreuzung.
Mit vorhandenem data/ds1_share_sector_years.csv rechnet das Skript nur die Tests neu (--rebuild liest alle Tage).
Ergebnis: data/ds1_share_sector_years.csv, data/ds1_share_test.csv, data/ds1_share_test.txt
Aufruf: python3 data/crecb_share.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import crecb_korea as K  # noqa: E402
from crec_filter import JP_FINE, JP_FINE_RX, JWORD, jp_fine_of  # noqa: E402
from crec_stats import perm_p  # noqa: E402
from crecb_salience import docs, tokens  # noqa: E402


def share_counts(w, cword, sect_rx):
    ci = np.array([i for i, x in enumerate(w) if cword.match(x)])
    r = {}
    for k, rx in sect_rx.items():
        si = [i for i, x in enumerate(w) if rx.match(x)]
        r[f"n_{k}"] = len(si)
        r[f"c_{k}"] = int(sum(np.any(np.abs(ci - x) <= 30) for x in si)) if len(ci) and si else 0
    return r


SYF = D / "ds1_share_sector_years.csv"
rows = []
for y, d, s, t in (docs() if (not SYF.exists() or "--rebuild" in sys.argv) else []):
    rj = share_counts(tokens(t), JWORD, JP_FINE_RX)
    rk = share_counts(tokens(K.DROP.sub(" ", t)), K.KWORD, K.KR_RX)
    rows += [{"challenger": "JP", "year": y, "sector": k[2:], "sector_words": rj[k], "near": rj["c_" + k[2:]]}
             for k in rj if k.startswith("n_")]
    rows += [{"challenger": "KR", "year": y, "sector": k[2:], "sector_words": rk[k], "near": rk["c_" + k[2:]]}
             for k in rk if k.startswith("n_")]
if rows:
    SY = pd.DataFrame(rows).groupby(["challenger", "sector", "year"], as_index=False)[["sector_words", "near"]].sum()
    SY["share_pct"] = (100 * SY.near / SY.sector_words.replace(0, np.nan)).round(3)
    SY.to_csv(SYF, index=False)
SY = pd.read_csv(SYF)
WORDS = pd.read_csv(D / "ds1_crecb_years.csv").groupby("year").words.sum()


def vol(s, a, b):
    """Sektorvolumen: Nennungen der Sektorwoerter je 1 Mio. Woerter aller Stichprobentage im Fenster."""
    w = WORDS[(WORDS.index >= a) & (WORDS.index <= b)].sum()
    z = s[(s.index >= a) & (s.index <= b)]
    return round(1e6 * z.sector_words.sum() / w, 1) if w else np.nan


def win(s, a, b):
    z = s[(s.index >= a) & (s.index <= b)]
    return round(100 * z.near.sum() / z.sector_words.sum(), 2) if len(z) and z.sector_words.sum() else np.nan


out, T = [], []
for ch, tab, win0 in (("JP", pd.read_csv(D / "ds1_crecb_test.csv"), (1960, 1975)),
                      ("KR", pd.read_csv(D / "ds1_kr_test.csv"), (1965, 1990))):
    for _, r in tab.iterrows():
        s = SY[(SY.challenger == ch) & (SY.sector == r.sector)].set_index("year")
        cy = int(r.crossover_year)
        pre = s[(s.index >= cy - 5) & (s.index <= cy - 1)]
        T.append({"challenger": ch, "sector": r.sector, "crossover_year": cy, "crossover_censored": r.crossover_censored,
                  "measure": r.measure, "measure_ids": r.measure_ids,
                  "sector_words_1955_1994": int(s[s.index <= 1994].sector_words.sum()),
                  "share_pre": win(s, cy - 5, cy - 1) if len(pre) >= 3 else np.nan,
                  "share_post": win(s, cy, cy + 4), "share_window": win(s, *win0),
                  "volume_pre": vol(s, cy - 5, cy - 1) if cy - 5 >= 1955 else np.nan,
                  "volume_post": vol(s, cy, cy + 4), "volume_window": vol(s, *win0)})
T = pd.DataFrame(T)
T.to_csv(D / "ds1_share_test.csv", index=False)
out.append("Anteil der Sektorwort-Nennungen mit dem Aufsteiger im Umkreis von 30 Woertern, in Prozent "
           "(Fenster: Japan 1960-1975, Korea 1965-1990)")
out.append(T.to_string(index=False))
for ch in ("JP", "KR"):
    z = T[T.challenger == ch]
    for col in ("share_window", "share_pre", "share_post", "volume_pre", "volume_post", "volume_window"):
        obs, p, k, n0 = perm_p(z[col], z.measure)
        out.append(f"{ch} {col}: mit Massnahme {z[z.measure][col].mean():.2f} (n={k}), ohne {z[~z.measure][col].mean():.2f} "
                   f"(n={n0}); Differenz {obs:+.2f}, exakter Permutationstest einseitig p = {p:.3f}")
(D / "ds1_share_test.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
