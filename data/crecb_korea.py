"""Korea im US-Kongress auf Basis der Stichprobentage (gebundener Record 1955-1994, taeglicher Record 1995-2025).

Gleiche Tage und gleiche Messung wie crecb_salience.py (Japan). Vor der Zaehlung werden Nennungen entfernt, die
nicht Suedkorea als Wirtschaft meinen: "North Korea(n)", "Democratic People's Republic of Korea", "Korean War",
"Korean conflict", "Korean peninsula". Korea zaehlt bei korea, korean(s), korea's, seoul.
Sektoren: verdraengte Gruppen Koreas (data/population_crossovers.csv, SITC Rev. 1 und Rev. 3); Kreuzungsjahr
= fruehestes Jahr ueber beide Klassifikationen (zensiert, wenn dieses zensiert ist). Breite Massnahmen gegen
Korea aus data/broad_register.csv (Codes SITC Rev. 1, Rev. 3 und HS4).
Ergebnis: data/ds1_kr_years.csv, data/ds1_kr_sector_years.csv, data/ds1_kr_test.csv, data/ds1_kr_test.txt
Aufruf: python3 data/crecb_korea.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from crec_filter import COMP  # noqa: E402
from crec_stats import perm_p  # noqa: E402
from crecb_salience import docs, near, tokens  # noqa: E402

DROP = re.compile(r"\b(north\s+korean?s?|north\s+korea's|democratic\s+people's\s+republic\s+of\s+korea|"
                  r"korean\s+(war|conflict|peninsula)|korea\s+war)\b", re.I)
KWORD = re.compile(r"^(korea|korean|koreans|korea's|seoul)$", re.I)
# Sektor: (Sektorwoerter, SITC Rev. 1, SITC Rev. 3, HS4)
KR = {
    "textiles": (r"^(textile|textiles|apparel|cotton|wool|woolen|yarn|fabric|fabrics|garment|garments|clothing|sweaters)$",
                 ["65", "841", "842"], ["65", "84"], []),
    "footwear": (r"^(footwear|shoe|shoes)$", ["851"], ["851"], []),
    "televisions": (r"^(television|televisions|tv|tvs)$", ["724"], ["761"], []),
    "steel": (r"^(steel|steelworkers|steelmakers|steelmaking)$", ["67"], ["67"], ["72", "7301", "7302", "7303", "7304", "7305", "7306"]),
    "washers": (r"^(washers|washing|appliances)$", [], ["775"], ["8450"]),
    "ships": (r"^(shipbuilding|shipyard|shipyards|shipbuilders)$", ["735"], ["793"], []),
    "telecom": (r"^(telecommunications|telecom|telephones|cellular)$", [], ["764"], []),
    "plywood": (r"^(plywood|veneer)$", ["631"], [], []),
    "leather": (r"^(leather|hides)$", ["611"], ["611"], []),
    "travel_goods": (r"^(luggage|handbags|suitcases)$", ["831"], ["831"], []),
    "glass_ceramics": (r"^(glass|glassware|ceramic|ceramics|pottery|tile|tiles)$", ["666"], ["666"], []),
    "toys": (r"^(toy|toys)$", ["894"], [], []),
    "metals": (r"^(copper|zinc|nickel)$", ["686"], ["682", "685", "686"], []),
    "optics": (r"^(optical|camera|cameras|lenses)$", ["863"], ["871"], []),
}
KR_RX = {k: re.compile(v[0], re.I) for k, v in KR.items()}


def kr_of(data, code):
    code = str(code)
    for k, (_, s1, s3, hs) in KR.items():
        pre = {"s1": s1, "s3": s3, "hs4": hs}[data]
        if any(code.startswith(p) for p in pre):
            return k
    return None


def measure(t):
    w = tokens(DROP.sub(" ", t))
    ki_ = [i for i, x in enumerate(w) if KWORD.match(x)]
    ci = [i for i, x in enumerate(w) if COMP.match(x)]
    r = {"words": len(w), "korea": len(ki_), "korea_comp": near(ki_, ci)}
    for k, rx in KR_RX.items():
        r[f"k_{k}"] = near(ki_, [i for i, x in enumerate(w) if rx.match(x)])
    return r


def main():
    X = pd.DataFrame([{"year": y, "day": d, "source": s, **measure(t)} for y, d, s, t in docs()])
    Y = X.groupby(["year", "source"]).agg(days=("day", "size"), **{c: (c, "sum") for c in X.columns
                                                                   if c not in ("year", "day", "source")}).reset_index()
    Y["korea_per_100k"] = (1e5 * Y.korea / Y.words).round(2)
    Y["korea_comp_per_1m"] = (1e6 * Y.korea_comp / Y.words).round(2)
    Y[["year", "source", "days", "words", "korea", "korea_comp", "korea_per_100k", "korea_comp_per_1m"]].to_csv(
        D / "ds1_kr_years.csv", index=False)
    SY = Y.melt(id_vars=["year", "words"], value_vars=[f"k_{k}" for k in KR], var_name="sector", value_name="korea_near")
    SY["sector"] = SY.sector.str[2:]
    SY.to_csv(D / "ds1_kr_sector_years.csv", index=False)

    cr = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
    cr = cr[cr.challenger == "KR"].copy()
    cr["sector"] = [kr_of(d, c) for d, c in zip(cr.data, cr.code)]
    reg = pd.read_csv(D / "broad_register.csv", dtype=str)
    reg = reg[reg.target.str.contains("KR")]
    T = []
    for k in KR:
        z = cr[cr.sector == k]
        if not len(z):
            continue
        cy = int(z.crossover_year.min())
        cens = bool(z[z.crossover_year == cy].left_censored.any())
        ms = []
        for _, r in reg.iterrows():
            codes = [(c, d) for col, d in (("codes_s1", "s1"), ("codes_s3", "s3"), ("codes_hs4", "hs4"))
                     for c in str(r[col]).split(";") if c != "nan"]
            if any(kr_of(d, c) == k for c, d in codes):
                ms.append((int(r.year), r.instrument_id))
        ms = sorted(ms)
        s = SY[SY.sector == k].set_index("year")
        pre = s[(s.index >= cy - 5) & (s.index <= cy - 1)]
        post = s[(s.index >= cy) & (s.index <= cy + 4)]
        w0 = s[(s.index >= 1965) & (s.index <= 1990)]
        rec = {"sector": k, "crossover_year": cy, "crossover_censored": cens, "n_groups": len(z), "measure": bool(ms),
               "measure_first_year": ms[0][0] if ms else None, "measure_ids": ";".join(i for _, i in ms),
               "voice_pre": round(1e6 * pre.korea_near.sum() / pre.words.sum(), 2) if len(pre) >= 3 else np.nan,
               "voice_post": round(1e6 * post.korea_near.sum() / post.words.sum(), 2) if len(post) else np.nan,
               "voice_1965_1990": round(1e6 * w0.korea_near.sum() / w0.words.sum(), 2)}
        T.append(rec)
    T = pd.DataFrame(T)
    T.to_csv(D / "ds1_kr_test.csv", index=False)
    out = [f"Stichprobentage {len(X)}; Woerter {int(X.words.sum()):,}"]
    per = pd.cut(Y.year, [1954, 1964, 1974, 1984, 1994, 2004, 2014, 2025])
    P = Y.groupby(per, observed=True)[["words", "korea", "korea_comp"]].sum()
    out.append("Periode | Korea je 100.000 W. | Korea nahe Wettbewerbswort je 1 Mio. W.")
    out += [f"{i} | {1e5*r.korea/r.words:.1f} | {1e6*r.korea_comp/r.words:.2f}" for i, r in P.iterrows()]
    out.append(T.to_string(index=False))
    A = T[~T.crossover_censored & T.voice_pre.notna()]
    out.append(f"Zeitfolge Korea: voice nach > vor in {(A.voice_post > A.voice_pre).sum()} von {len(A)} Sektoren")
    for col in ["voice_1965_1990", "voice_pre", "voice_post"]:
        obs, p, k, n0 = perm_p(T[col], T.measure)
        out.append(f"Auswahl Korea {col}: mit Massnahme {T[T.measure][col].mean():.2f} (n={k}), ohne "
                   f"{T[~T.measure][col].mean():.2f} (n={n0}); Differenz {obs:+.2f}, p = {p:.3f}")
    (D / "ds1_kr_test.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    print("\n".join(out))


if __name__ == "__main__":
    main()
