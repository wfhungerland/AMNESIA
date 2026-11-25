"""Referee points 3 and 4: timing tests by export crossover, without the advanced-chips 'milestone', and at the
level of milestones instead of responses.

Inputs: data/ds1_events.csv, data/tests_initiation.csv (from tests_initiation.py).
Output: data/tests_robust_timing.txt
"""
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
e = pd.read_csv(D / "ds1_events.csv")
e = e[e.case != "JPGB"].copy()
e["binding"] = e.type.str.startswith("binding") | (e.type == "denial")
ti = pd.read_csv(D / "tests_initiation.csv").set_index("response_id")
e["init_year"] = e.response_id.map(ti.init_year)
out = []


def window(lag):
    return int(((lag >= -10) & (lag <= -1)).sum()), int(((lag >= 0) & (lag <= 9)).sum())


def binom_lo(k, n):  # P(X <= k), p = 0.5
    return sum(comb(n, i) for i in range(k + 1)) / 2 ** n


rng = np.random.default_rng(20261125)


def test(sub, lag, key, label):
    pre, post = window(lag)
    ms = sub[key].unique()
    st = []
    for _ in range(10000):
        sh = dict(zip(ms, rng.integers(-10, 11, len(ms))))
        a, b = window(lag - sub[key].map(sh))
        st.append(b / (a + b) if a + b else np.nan)
    st = np.array(st)
    obs = post / (pre + post) if pre + post else np.nan
    out.append(f"{label}: N={len(sub)}, before {int((lag < 0).sum())}, from {int((lag >= 0).sum())}; window {pre}/{post}, "
               f"binomial p={binom_lo(pre, pre + post):.4f}; placebo mean {np.nanmean(st):.2f}, p={np.nanmean(st >= obs):.4f}")


# (3a) without the advanced-chips milestone (capability, not displacement)
x = e[e.sector_milestone != "M-CN-CHIP"]
out.append("(3a) Without the advanced-chips milestone (M-CN-CHIP):")
for lab, sub in [("all responses", x), ("binding", x[x.binding]), ("broad (IR >= 4)", x[x.reach_coder1 >= 4])]:
    test(sub, sub.year - sub.milestone_year, "sector_milestone", f"  measure dates, {lab}")
    test(sub, sub.init_year.fillna(sub.year) - sub.milestone_year, "sector_milestone", f"  initiation dates, {lab}")

# (3b) export crossover as the primary measure: responses with an exactly dated crossover
out += ["", "(3b) Export crossover instead of the milestone (responses with an exact crossover year):"]
c = e[e.export_year_type == "genau"].copy()
c["export_year"] = c.export_year.astype(float)
out.append(f"  classification of all 41: {e.phase_export.value_counts().to_dict()}")
for lab, sub in [("all responses", c), ("binding", c[c.binding]), ("broad (IR >= 4)", c[c.reach_coder1 >= 4])]:
    test(sub, sub.year - sub.export_year, "sector_milestone", f"  measure dates, {lab}")
    test(sub, sub.init_year.fillna(sub.year) - sub.export_year, "sector_milestone", f"  initiation dates, {lab}")

# (4) milestone-level test: does the first binding response of each milestone come from the milestone onwards?
out += ["", "(4) One observation per milestone: first binding response relative to the milestone (sign test, p = 0.5):"]
b = e[e.binding]
for lab, col in [("measure dates", "year"), ("initiation dates", "init_year")]:
    for excl in (False, True):
        g = b if not excl else b[b.sector_milestone != "M-CN-CHIP"]
        g = g.assign(t=g[col].fillna(g.year))
        first = g.groupby("sector_milestone").apply(lambda z: z.t.min() - z.milestone_year.iloc[0], include_groups=False)
        n, k = len(first), int((first >= 0).sum())
        p = 1 - binom_lo(k - 1, n)
        out.append(f"  {lab}{' (without chips)' if excl else ''}: {k} of {n} milestones have their first binding response from the "
                   f"milestone onwards; one-sided p={p:.4f}; lags of the first response: {sorted(first.astype(int).tolist())}")
(D / "tests_robust_timing.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
