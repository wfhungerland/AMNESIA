"""Tests der Reihenfolge (Revision nach Panel-Review).

1. Ereignisfenster: Reaktionen in den 10 Jahren vor gegen die 10 Jahre ab dem Meilenstein (Binomialtest, p = 0,5).
2. Placebo: alle Meilensteine zufaellig um -10 bis +10 Jahre verschoben (10.000 Ziehungen); Anteil der
   Ziehungen, deren Vor-/Nach-Verhaeltnis mindestens so einseitig ist wie das beobachtete.
3. Bruchtest Hansard: Jahr(e) mit bestem Strukturbruch im Niveau von log(1 + Nennungen je 100.000 Woerter),
   ohne vorgegebene Bruchjahre (kleinste Fehlerquadratsumme; 1 bis 3 Brueche, Auswahl per BIC).
Ergebnis: data/tests_sequence.txt
"""
from math import comb, log
from pathlib import Path
import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
e = pd.read_csv(D / "ds1_events.csv")
e["binding"] = e.type.str.startswith("binding") | (e.type == "denial")
out = []

def window(df, lag):
    pre = ((lag >= -10) & (lag <= -1)).sum()
    post = ((lag >= 0) & (lag <= 9)).sum()
    return int(pre), int(post)

def binom_p(k_pre, n):  # einseitig: P(X <= k_pre) bei p = 0.5
    return sum(comb(n, i) for i in range(0, k_pre + 1)) / 2 ** n

rng = np.random.default_rng(20261121)
for label, sub in [("alle Reaktionen", e), ("bindende Reaktionen", e[e.binding])]:
    pre, post = window(sub, sub.lag_years)
    p = binom_p(pre, pre + post)
    # Placebo: Verschiebung je Meilenstein, gleiche Verschiebung fuer alle Reaktionen dieses Meilensteins
    ms = sub.sector_milestone.unique()
    stats = []
    for _ in range(10000):
        shift = dict(zip(ms, rng.integers(-10, 11, len(ms))))
        lag = sub.lag_years - sub.sector_milestone.map(shift)
        a, b = window(sub, lag)
        stats.append(b / (a + b) if a + b else np.nan)
    stats = np.array(stats)
    obs = post / (pre + post)
    p_pl = float(np.nanmean(stats >= obs))
    out.append(f"{label}: 10 Jahre davor {pre}, 10 Jahre ab Meilenstein {post}; Anteil danach {obs:.2f}; "
               f"Binomial p = {p:.4f}; Placebo: mittlerer Anteil {np.nanmean(stats):.2f}, p = {p_pl:.4f}")

# Bruchtest
h = pd.read_csv(D / "ds1_hansard_salience.csv").sort_values("year")
y = np.log1p(h.germany_hits_per_100k_words.values)
yrs = h.year.values
n = len(y)
def sse(a, b):
    s = y[a:b]
    return ((s - s.mean()) ** 2).sum()
best = {}
minseg = 5
# dynamische Programmierung fuer bis zu 3 Brueche
import itertools
for k in (1, 2, 3):
    bestk = None
    for bp in itertools.combinations(range(minseg, n - minseg + 1), k):
        if any(b2 - b1 < minseg for b1, b2 in zip(bp, bp[1:])):
            continue
        pts = (0,) + bp + (n,)
        s = sum(sse(a, b) for a, b in zip(pts, pts[1:]))
        if bestk is None or s < bestk[0]:
            bestk = (s, bp)
    best[k] = bestk
s0 = sse(0, n)
bic = {0: n * log(s0 / n)}
for k, (s, bp) in best.items():
    bic[k] = n * log(s / n) + (2 * k + 1) * log(n)
kbest = min(bic, key=bic.get)
for k in (1, 2, 3):
    out.append(f"Hansard, {k} Bruch/Brueche: Bruchjahre {[int(yrs[b]) for b in best[k][1]]}, BIC {bic[k]:.1f}")
out.append(f"Hansard, BIC ohne Bruch {bic[0]:.1f}; beste Zahl der Brueche: {kbest}")
(D / "tests_sequence.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
