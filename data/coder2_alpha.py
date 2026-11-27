"""Agreement between the two coders of the reach score, and the main counts with the second coder's scores.

Call: python3 data/coder2_alpha.py path/to/coding_sheet_coder2.xlsx (or .csv)
Output: data/coder2/alpha.txt, data/coder2/disagreements.csv
Krippendorff's alpha, ordinal metric (Krippendorff 2013, ch. 12), two coders, no missing values in paired items.
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
O = D / "coder2"


def alpha_ordinal(a, b, levels=(1, 2, 3, 4, 5)):
    idx = {v: i for i, v in enumerate(levels)}
    k = len(levels)
    o = np.zeros((k, k))
    for x, y in zip(a, b):  # each unit with two values adds both ordered pairs, weight 1/(m-1) = 1
        o[idx[x], idx[y]] += 1
        o[idx[y], idx[x]] += 1
    nc = o.sum(1)
    n = nc.sum()
    d2 = np.zeros((k, k))
    for c in range(k):
        for j in range(k):
            lo, hi = min(c, j), max(c, j)
            d2[c, j] = (nc[lo:hi + 1].sum() - (nc[lo] + nc[hi]) / 2) ** 2
    de = (np.outer(nc, nc) * d2).sum()
    return 1.0 if de == 0 else 1 - (n - 1) * (o * d2).sum() / de


def main(path):
    K = pd.read_csv(O / "key.csv")
    s = pd.read_csv(path) if str(path).endswith(".csv") else pd.read_excel(path, sheet_name="coding")
    s = s.rename(columns={c: "coder2" for c in s.columns if str(c).startswith("IR")})[["item", "coder2"]]
    X = K.merge(s, on="item")
    miss = X.coder2.isna().sum()
    X = X.dropna(subset=["coder2"]).assign(coder2=lambda z: z.coder2.astype(int))
    out = [f"Items scored: {len(X)} of {len(K)} (missing {miss})"]
    for lab, g in [("all items", X), ("responses", X[X.set == "responses"]), ("register", X[X.set == "register"])]:
        a = alpha_ordinal(g.coder1, g.coder2)
        same = (g.coder1 == g.coder2).mean()
        broad = ((g.coder1 >= 4) == (g.coder2 >= 4)).mean()
        out.append(f"{lab}: N={len(g)}, ordinal alpha {a:.3f}, exact agreement {same:.2f}, agreement on broad (IR >= 4) {broad:.2f}")
    # main counts with the second coder's scores
    e = pd.read_csv(D / "ds1_events.csv")
    e = e[e.case != "JPGB"].merge(X[X.set == "responses"][["orig_id", "coder2"]], left_on="response_id", right_on="orig_id")
    for col, lab in [("reach_coder1", "coder 1"), ("coder2", "coder 2")]:
        for thr, name in [(3, "binding (IR >= 3)"), (4, "broad (IR >= 4)")]:
            g = e[e[col] >= thr]
            out.append(f"{lab}, {name}: {len(g)} responses, {int((g.lag_years < 0).sum())} before the milestone")
    both = e[(e.reach_coder1 >= 4) & (e.coder2 >= 4)]
    out.append(f"broad for both coders: {len(both)} responses, {int((both.lag_years < 0).sum())} before the milestone")
    X[X.coder1 != X.coder2].to_csv(O / "disagreements.csv", index=False)
    (O / "alpha.txt").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
