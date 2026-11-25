"""Referee point 2: timing tests with the date on which the process behind each binding response began.

Initiation dates: data/ds1_initiation.csv (petition filed, investigation opened, bill introduced, negotiations opened).
Where a start could not be verified, the measure date is kept. Non-binding responses keep their dates.
Tests as in tests_sequence.py: window of ten years either side of the milestone (one-sided binomial test) and a
placebo that shifts every milestone by -10 to +10 years (10,000 draws). Output: data/tests_initiation.txt
"""
from math import comb
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
e = pd.read_csv(D / "ds1_events.csv")
e = e[e.case != "JPGB"].copy()
e["binding"] = e.type.str.startswith("binding") | (e.type == "denial")
ini = pd.read_csv(D / "ds1_initiation.csv", dtype=str).set_index("response_id")
iy = pd.to_numeric(ini.initiation_date.str[:4], errors="coerce")
e["init_year"] = e.response_id.map(iy)
e["init_year"] = e.init_year.fillna(e.year)
e["lag_init"] = e.init_year - e.milestone_year
out = [f"Binding responses with an initiation date: {int(e.response_id.isin(ini.index).sum())}; "
       f"not verified, measure date kept: {', '.join(ini.index[iy.isna()])}"]


def window(lag):
    return int(((lag >= -10) & (lag <= -1)).sum()), int(((lag >= 0) & (lag <= 9)).sum())


def binom_p(k, n):
    return sum(comb(n, i) for i in range(k + 1)) / 2 ** n


rng = np.random.default_rng(20261121)
for col, lab in [("lag_years", "measure dates"), ("lag_init", "initiation dates")]:
    for name, sub in [("all responses", e), ("binding responses", e[e.binding]), ("broad responses (IR >= 4)", e[e.reach_coder1 >= 4])]:
        pre, post = window(sub[col])
        ms = sub.sector_milestone.unique()
        st = []
        for _ in range(10000):
            sh = dict(zip(ms, rng.integers(-10, 11, len(ms))))
            a, b = window(sub[col] - sub.sector_milestone.map(sh))
            st.append(b / (a + b) if a + b else np.nan)
        st = np.array(st)
        obs = post / (pre + post)
        out.append(f"{lab}, {name}: before {int((sub[col] < 0).sum())}, from the milestone {int((sub[col] >= 0).sum())}; "
                   f"window -10..-1 / 0..9: {pre} / {post}, share after {obs:.2f}, binomial p = {binom_p(pre, pre + post):.4f}; "
                   f"placebo mean {np.nanmean(st):.2f}, p = {np.nanmean(st >= obs):.4f}")
b = e[e.binding]
moved = b[(b.lag_years >= 0) & (b.lag_init < 0)]
out += ["", "Binding responses whose process began before the milestone although the measure came after it:"]
for _, r in moved.iterrows():
    out.append(f"  {r.response_id} (IR {int(r.reach_coder1)}): initiation {ini.loc[r.response_id, 'initiation_date']}, "
               f"measure {r.date}, milestone {int(r.milestone_year)}; {r.description}")
d = (b.year - b.init_year)
out += ["", f"Delay from initiation to measure, binding responses: median {d.median():.1f} years, mean {d.mean():.1f}, max {d.max():.0f}",
        f"Lags from initiation, binding responses: median {b.lag_init.median():.1f}, range {b.lag_init.min():.0f} to {b.lag_init.max():.0f}"]
for c, g in b.groupby("case"):
    post = g[g.lag_init >= 0]
    out.append(f"  {c}: {len(g)} binding, {int((g.lag_init < 0).sum())} begun before the milestone; lags from initiation of those after: "
               f"{post.lag_init.min():.0f} to {post.lag_init.max():.0f}")
e[["response_id", "case", "milestone_year", "year", "init_year", "lag_years", "lag_init", "reach_coder1"]].to_csv(D / "tests_initiation.csv", index=False)
(D / "tests_initiation.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
