"""Second coding by language models: agreement with the first coder and among the models.

Inputs: data/coder2/models/<model>.csv (item, IR, doubt), answers to data/coder2/PROMPT.md, pasted by the author on
26 November 2026; data/coder2/key.csv. Claude is reported separately, because the first coding was prepared with
the help of Claude. Consensus: median of the four other models, ties resolved downwards (rule for doubtful cases).
Output: data/coder2/models_alpha.txt, data/coder2/models_disagreements.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
O = D / "coder2"
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


K = pd.read_csv(O / "key.csv")
models = ["chatgpt", "gemini", "grok", "deepseek", "claude"]
for m in models:
    x = pd.read_csv(O / "models" / f"{m}.csv")
    K = K.merge(x[["item", "IR"]].rename(columns={"IR": m}), on="item")
others = models[:4]
K["consensus"] = [int(np.floor(np.median(r))) if np.median(r) % 1 == 0 else int(np.floor(np.median(r)))
                  for r in K[others].values]
out = [f"Items: {len(K)} (responses {int((K.set == 'responses').sum())}, register {int((K.set == 'register').sum())})", ""]
out.append("Ordinal alpha and agreement with the first coder:")
for m in models + ["consensus"]:
    for lab, g in [("all", K), ("responses", K[K.set == "responses"]), ("register", K[K.set == "register"])]:
        a = alpha_ordinal(g[["coder1", m]].values.tolist())
        out.append(f"  {m:9s} {lab:9s}: alpha {a:.3f}, exact {np.mean(g.coder1 == g[m]):.2f}, "
                   f"broad (IR>=4) {np.mean((g.coder1 >= 4) == (g[m] >= 4)):.2f}")
out += ["", f"Alpha among the four other models: {alpha_ordinal(K[others].values.tolist()):.3f}",
        f"Alpha among the four other models and the first coder: {alpha_ordinal(K[others + ['coder1']].values.tolist()):.3f}"]

e = pd.read_csv(D / "ds1_events.csv")
e = e[e.case != "JPGB"].merge(K[K.set == "responses"][["orig_id", "consensus"]], left_on="response_id", right_on="orig_id")
out += ["", "Main counts (41 core responses), first coder against model consensus:"]
for col in ("reach_coder1", "consensus"):
    for thr, name in [(3, "binding (IR >= 3)"), (4, "broad (IR >= 4)")]:
        g = e[e[col] >= thr]
        out.append(f"  {col}, {name}: {len(g)} responses, {int((g.lag_years < 0).sum())} before the milestone, "
                   f"{int((g.lag_years >= 0).sum())} from it")
both = e[(e.reach_coder1 >= 4) & (e.consensus >= 4)]
out.append(f"  broad for both: {len(both)}, before the milestone {int((both.lag_years < 0).sum())}")
reg = K[K.set == "register"]
out.append(f"Register of broad measures (42 entries): consensus scores IR >= 4 for {int((reg.consensus >= 4).sum())}, "
           f"IR 3 for {int((reg.consensus == 3).sum())}, IR <= 2 for {int((reg.consensus <= 2).sum())}")
d = K[K.coder1 != K.consensus][["item", "orig_id", "set", "measure", "coder1"] + others + ["consensus", "claude"]]
d.to_csv(O / "models_disagreements.csv", index=False)
out += ["", f"Items where the consensus differs from the first coder: {len(d)}"]
out += [f"  {r.orig_id}: coder1 {r.coder1}, consensus {r.consensus} ({', '.join(f'{m} {getattr(r, m)}' for m in others)}): {r.measure[:80]}"
        for r in d.itertuples()]
(O / "models_alpha.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
