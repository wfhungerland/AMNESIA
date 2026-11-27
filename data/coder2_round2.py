"""Second coding, round 2: four blind codings of the 108 items of data/coder2/coding_sheet.csv (incl. the 18 sweep
entries C91-C108), pasted by the author on 27 November 2026 (coders A-D; source not recorded in the files).
Output: data/coder2/round2/alpha.txt, data/coder2/round2/disagreements.csv
"""
from pathlib import Path
import numpy as np
import pandas as pd

LEV = (1, 2, 3, 4, 5)


def alpha_ordinal(units, levels=LEV):
    """Krippendorff's alpha, ordinal; units = list of value lists (one value per coder)."""
    idx = {v: i for i, v in enumerate(levels)}
    k = len(levels)
    o = np.zeros((k, k))
    for vals in units:
        vals = [v for v in vals if not pd.isna(v)]
        m = len(vals)
        if m < 2:
            continue
        for a in range(m):
            for b in range(m):
                if a != b:
                    o[idx[int(vals[a])], idx[int(vals[b])]] += 1 / (m - 1)
    nc = o.sum(1)
    n = nc.sum()
    d2 = np.array([[(nc[min(c, j):max(c, j) + 1].sum() - (nc[c] + nc[j]) / 2) ** 2 for j in range(k)] for c in range(k)])
    de = (np.outer(nc, nc) * d2).sum()
    return 1 - (n - 1) * (o * d2).sum() / de


O = Path(__file__).resolve().parent / "coder2"
K = pd.read_csv(O / "key.csv")
C = list("ABCD")
for c in C:
    x = pd.read_csv(O / "round2" / f"coder_{c}.csv")
    K = K.merge(x[["item", "IR"]].rename(columns={"IR": c}), on="item")
K["median"] = np.floor(K[C].median(axis=1)).astype(int)
K["sweep"] = K.item.str[1:].astype(int) > 90
out = [f"Items: {len(K)}"]
for m in C + ["median"]:
    for lab, g in [("all", K), ("responses", K[K.set == "responses"]), ("register", K[K.set == "register"]), ("sweep C91-C108", K[K.sweep])]:
        a = alpha_ordinal(g[["coder1", m]].values.tolist())
        out.append(f"  {m:6s} {lab:15s}: N={len(g):3d} alpha {a:.3f}, exact {np.mean(g.coder1 == g[m]):.2f}, broad (IR>=4) {np.mean((g.coder1 >= 4) == (g[m] >= 4)):.2f}")
out += ["", f"Alpha among A-D: {alpha_ordinal(K[C].values.tolist()):.3f}; A-D and first coder: {alpha_ordinal(K[C + ['coder1']].values.tolist()):.3f}"]
for lab, g in [("responses", K[K.set == "responses"]), ("register", K[K.set == "register"])]:
    out.append(f"Broad (IR>=4), {lab}: first coder {int((g.coder1 >= 4).sum())}, median of A-D {int((g['median'] >= 4).sum())}, "
               + ", ".join(f"{c} {int((g[c] >= 4).sum())}" for c in C))
d = K[(K.coder1 >= 4) != (K["median"] >= 4)]
out += ["", "Items where first coder and median of A-D differ on broad (IR>=4):"] + \
       [f"  {r.item} {r.orig_id} coder1 {r.coder1} median {r.median} ({r.A},{r.B},{r.C},{r.D}): {r.measure[:90]}" for r in d.itertuples()]
K[K.coder1 != K["median"]].to_csv(O / "round2" / "disagreements.csv", index=False)
(O / "round2" / "alpha.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
