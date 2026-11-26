"""Recomputes the register-based outcome columns of the two panels after a change of reach scores.

population_panel.py and cases_test.py build the panels from raw trade data, which are not redistributed. The outcome
columns (start of a targeted broad measure, groups at risk) depend only on the register and on the group codes,
so they can be recomputed from the stored panels. Only register entries with IR >= 4 count as broad.
Check: with the original reach scores (reach_original) the stored columns were reproduced exactly (first run, 26 Nov 2026).
Output: overwrites the outcome columns of data/population_panel.csv and data/cases_panel.csv.
"""
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
COL = {"s1": "codes_s1", "s3": "codes_s3", "hs4": "codes_hs4"}


def covers(r, data, code):
    cs = r[COL[data]] if isinstance(r[COL[data]], str) else ""
    return cs == "ALL" or any(code.startswith(k) for k in cs.split(";") if k)


def outcomes(P, reg, glob):
    hits = {}
    for t, d, c in P[["challenger", "data", "code"]].drop_duplicates().itertuples(index=False):
        hits[(t, d, c)] = sorted(int(r.year) for _, r in reg.iterrows()
                                 if t in r.target.split(";") and r.instrument_id not in glob and covers(r, d, c))
    key = list(zip(P.challenger, P.data, P.code, P.year))
    broad = [int(y in hits[(t, d, c)]) for t, d, c, y in key]
    risk = [int(not any(h < y for h in hits[(t, d, c)])) for t, d, c, y in key]
    return broad, risk


if __name__ == "__main__":
    reg0 = pd.read_csv(D / "broad_register.csv", dtype=str)
    for name, glob, extra in [("population_panel.csv", {"B-02", "B-17", "B-19"}, True),
                              ("cases_panel.csv", {"B-02", "B-17", "B-19", "B-34", "B-31"}, False)]:
        P = pd.read_csv(D / name, dtype={"code": str})
        for col, cur in (("reach_original", "check"), ("reach", "new")):
            reg = reg0[reg0[col].astype(int) >= 4]
            b, a = outcomes(P, reg, glob)
            if extra:
                bx, ax = outcomes(P, reg, glob | {"B-20"})
            if cur == "check":
                ok = (P.broad.tolist() == b) and (P.at_risk.tolist() == a)
                if extra:
                    ok = ok and P.broad_x301.tolist() == bx and P.at_risk_x301.tolist() == ax
                print(f"{name}: original scores reproduce stored columns: {ok} (False on a rerun after recoding)")
            else:
                print(f"{name}: broad starts {int(P.broad.sum())} -> {sum(b)}")
                P["broad"], P["at_risk"] = b, a
                if extra:
                    P["broad_x301"], P["at_risk_x301"] = bx, ax
        P.to_csv(D / name, index=False)
