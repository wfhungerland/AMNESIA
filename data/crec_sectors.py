"""Sektorale Kongressmessung China und Test: Sagt die Aufmerksamkeit fuer einen Sektor eine breite Massnahme voraus?

Laeuft nach crec_salience.py, nur auf dem Zwischenspeicher. Analog zu hansard_sectors.py:
eine Wirtschaftsdebatte gehoert zu einem Feinsektor (data/crec_filter.py, FINE), wenn sie mindestens
3 Sektorwoerter enthaelt; sie verbindet China mit dem Sektor, wenn ein China-Wort hoechstens 30 Woerter
von einem Sektorwort entfernt steht.

Kreuzungsjahr des Sektors: fruehestes nicht linkszensiertes Kreuzungsjahr seiner Warengruppen in
data/population_crossovers.csv (China, SITC Rev. 3 und HS4); sind alle zensiert, gilt "spaetestens" das
frueheste Jahr. Breite Massnahme: sektorspezifisches Instrument gegen China in data/broad_register.csv
(ohne B-20, die Section-301-Zoelle auf alle Warengruppen), zugeordnet ueber die HS4- und SITC-Codes.
Aufmerksamkeit (voice): mit China verbundene Sektordebatten je 1.000 Wirtschaftsdebatten,
in den 5 Jahren vor dem Kreuzungsjahr (vor) und ab dem Kreuzungsjahr (5 Jahre, nach); dazu ein festes
Kalenderfenster 2001-2017 (nach dem WTO-Beitritt, vor den Massnahmen von 2018-2024), gleich fuer alle Sektoren.

Ergebnis: data/ds1_crec_sectors.csv (Debatte x Sektor), data/ds1_crec_sector_years.csv (Sektor x Jahr),
data/ds1_crec_voice_test.csv (Sektor), data/ds1_crec_voice_test.txt
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from crec_filter import FINE, FINE_RX, SECT_RX, TWORD, fine_of, sector_of  # noqa: E402
from crec_salience import text, wilson  # noqa: E402
from crec_stats import perm_p  # noqa: E402

# 1. Debatte x Sektor
g = pd.read_csv(D / "ds1_crec_granules.csv", usecols=["year", "granule", "loaded"])
g = g[g.loaded]
rows, rows_c = [], []
for yr, gid in zip(g.year, g.granule):
    t = text(gid)
    if t is None:
        continue
    t = re.sub(r"\belectric\s+vehicle", "electric-vehicle", t, flags=re.I)
    w = [re.sub(r"[^\w'-]", "", x) for x in t.split()]
    ti = [i for i, x in enumerate(w) if TWORD.match(x)]
    for k, rx in FINE_RX.items():
        si = [i for i, x in enumerate(w) if rx.match(x)]
        if len(si) >= 3:
            near = bool(ti) and any(abs(a - b) <= 30 for a in ti for b in si)
            rows.append({"year": yr, "granule": gid, "sector": k, "sector_words": len(si), "china_near": near})
    for k, rx in SECT_RX.items():
        si = [i for i, x in enumerate(w) if rx.match(x)]
        if len(si) >= 3:
            rows_c.append({"year": yr, "group": k, "china_near": bool(ti) and any(abs(a - b) <= 30 for a in ti for b in si)})
S = pd.DataFrame(rows)
S.to_csv(D / "ds1_crec_sectors.csv", index=False)
econ = g.groupby("year").size()
SY = (S.groupby(["sector", "year"]).agg(debates=("granule", "size"), china_linked=("china_near", "sum"))
      .reset_index())
SY = (pd.MultiIndex.from_product([list(FINE), sorted(econ.index)], names=["sector", "year"]).to_frame(index=False)
      .merge(SY, how="left").fillna(0))
SY["econ_granules"] = SY.year.map(econ)
SY["linked_per_1000_econ"] = (1000 * SY.china_linked / SY.econ_granules).round(3)
SY.to_csv(D / "ds1_crec_sector_years.csv", index=False)

# 2. Kreuzungsjahr und Massnahme je Sektor
cr = pd.read_csv(D / "population_crossovers.csv", dtype={"code": str})
cr = cr[cr.challenger == "CN"].copy()
cr["sector"] = [fine_of(d, c) for d, c in zip(cr.data, cr.code)]
reg = pd.read_csv(D / "broad_register.csv", dtype=str)
reg = reg[reg.target.str.contains("CN") & (reg.instrument_id != "B-20")]
pw = pd.read_csv(D / "population_weight.csv", dtype={"code": str})
pw = pw[pw.challenger == "CN"].copy()
pw["sector"] = [fine_of(d, c) for d, c in zip(pw.data, pw.code)]


def measures(sector):
    _, hs, s3 = FINE[sector]
    out = []
    for _, r in reg.iterrows():
        codes = [(c, "hs4") for c in str(r.codes_hs4).split(";") if c != "nan"] + \
                [(c, "s3") for c in str(r.codes_s3).split(";") if c != "nan"]
        if any(fine_of(d, c) == sector for c, d in codes):
            out.append((int(r.year), r.instrument_id))
    return sorted(out)


T = []
for k in FINE:
    z = cr[cr.sector == k]
    unc = z[~z.left_censored]
    if len(unc):
        cy, cens = int(unc.crossover_year.min()), False
    elif len(z):
        cy, cens = int(z.crossover_year.min()), True
    else:
        cy, cens = None, False
    m = measures(k)
    sy = SY[SY.sector == k].set_index("year")
    rec = {"sector": k, "crossover_year": cy, "crossover_censored": cens, "n_codes_crossed": len(z),
           "measure": bool(m), "measure_first_year": m[0][0] if m else None,
           "measure_ids": ";".join(i for _, i in m), "debates_1995_2025": int(sy.debates.sum()),
           "china_linked_1995_2025": int(sy.china_linked.sum())}
    if cy is not None:
        pre = sy.loc[(sy.index >= cy - 5) & (sy.index <= cy - 1)]
        post = sy.loc[(sy.index >= cy) & (sy.index <= cy + 4)]
        rec["voice_pre"] = round(1000 * pre.china_linked.sum() / pre.econ_granules.sum(), 2) if len(pre) >= 3 else np.nan
        rec["voice_post"] = round(1000 * post.china_linked.sum() / post.econ_granules.sum(), 2) if len(post) else np.nan
        rec["pre_years"] = len(pre)
        b = sy.loc[sy.index < cy]
        a = sy.loc[sy.index >= cy]
        rec["linked_share_before"] = round(100 * b.china_linked.sum() / b.debates.sum(), 1) if b.debates.sum() else np.nan
        rec["debates_before"] = int(b.debates.sum())
        rec["linked_share_after"] = round(100 * a.china_linked.sum() / a.debates.sum(), 1) if a.debates.sum() else np.nan
        rec["debates_after"] = int(a.debates.sum())
    w0 = sy.loc[(sy.index >= 2001) & (sy.index <= 2017)]
    rec["voice_2001_2017"] = round(1000 * w0.china_linked.sum() / w0.econ_granules.sum(), 2)
    q = pw[pw.sector == k]
    rec["l_m_us_mean"] = round(q.l_m_us.mean(), 2) if len(q) else np.nan
    rec["l_emp_mean"] = round(q.l_emp.mean(), 2) if len(q) else np.nan
    if m and cy is not None:
        mw = sy.loc[(sy.index >= m[0][0] - 5) & (sy.index <= m[0][0] - 1)]
        rec["voice_5y_before_measure"] = round(1000 * mw.china_linked.sum() / mw.econ_granules.sum(), 2) if len(mw) else np.nan
    T.append(rec)
T = pd.DataFrame(T)
T.to_csv(D / "ds1_crec_voice_test.csv", index=False)


out = ["Sektoren (Kreuzung China ueber USA im Welthandel; Massnahme = sektorspezifisches breites Instrument ohne 301-Zoelle 2018)"]
show = ["sector", "crossover_year", "crossover_censored", "measure_ids", "debates_1995_2025", "china_linked_1995_2025",
        "linked_share_before", "debates_before", "linked_share_after", "debates_after", "voice_pre", "voice_post",
        "voice_5y_before_measure", "voice_2001_2017", "l_m_us_mean", "l_emp_mean"]
out.append(T[show].to_string(index=False))

# Test A: Zeitfolge, gepoolt ueber Sektoren mit unzensierter Kreuzung ab 2000 (Vorlauf im Record vorhanden)
A = T[(~T.crossover_censored) & (T.crossover_year >= 2000)]
kb = sum(int(SY[(SY.sector == s) & (SY.year < c)].china_linked.sum()) for s, c in zip(A.sector, A.crossover_year))
nb = sum(int(SY[(SY.sector == s) & (SY.year < c)].debates.sum()) for s, c in zip(A.sector, A.crossover_year))
ka = sum(int(SY[(SY.sector == s) & (SY.year >= c)].china_linked.sum()) for s, c in zip(A.sector, A.crossover_year))
na = sum(int(SY[(SY.sector == s) & (SY.year >= c)].debates.sum()) for s, c in zip(A.sector, A.crossover_year))
lo, hi = wilson(kb, nb)
lo2, hi2 = wilson(ka, na)
out.append(f"\nTest A (Zeitfolge), {len(A)} Sektoren mit Kreuzung 2000 oder spaeter: China verbunden vor der Kreuzung "
           f"{100*kb/nb:.1f} % von {nb} Sektordebatten [{lo:.1f}-{hi:.1f}], ab der Kreuzung {100*ka/na:.1f} % von {na} [{lo2:.1f}-{hi2:.1f}]")
up = (A.voice_post > A.voice_pre).sum()
out.append(f"   voice nach > voice vor in {up} von {A[['voice_pre','voice_post']].dropna().shape[0]} Sektoren")

# Test B: Auswahl. Haben Sektoren mit spaeterer breiter Massnahme mehr Aufmerksamkeit?
for col in ["voice_2001_2017", "voice_pre", "voice_post", "china_linked_1995_2025", "l_m_us_mean", "l_emp_mean"]:
    obs, p, k, n0 = perm_p(T[col], T.measure)
    out.append(f"Test B {col}: Mittel mit Massnahme {T[T.measure][col].mean():.2f} (n={k}), ohne {T[~T.measure][col].mean():.2f} "
               f"(n={n0}); Differenz {obs:+.2f}, exakter Permutationstest einseitig p = {p:.3f}")
# Robustheit: Reifen (Section 421, 2009) und Textil (Schutzmassnahmen 2005) als Sektoren mit Massnahme.
# Nicht im Register (Auswahlregel: Section 201 mit Mengengrenzen); das Register bleibt unveraendert.
T["measure_robust"] = T.measure | T.sector.isin(["tires", "textiles_apparel"])
for col in ["voice_2001_2017", "voice_pre", "voice_post"]:
    obs, p, k, n0 = perm_p(T[col], T.measure_robust)
    out.append(f"Robustheit (Reifen und Textil mit Massnahme) {col}: Differenz {obs:+.2f}, p = {p:.3f} (n={k} gegen {n0})")

# Test C: Abstufung der 301-Zoelle (data/ds1_301_hs4.csv). Anteil der HTS8-Positionen einer HS4-Gruppe auf
# den Listen 1 und 2 (25 % ab Juli/August 2018) und Erhoehung in der Ueberpruefung 2024.
from scipy.stats import spearmanr  # noqa: E402
import statsmodels.formula.api as smf  # noqa: E402
L = pd.read_csv(D / "ds1_301_hs4.csv", dtype={"hs4": str})
L = L[L.lines > 0]
fs = []
for k in FINE:
    z = L[[fine_of("hs4", c) == k for c in L.hs4]]
    fs.append({"sector": k, "share_12": z.share_12.mean() if len(z) else np.nan,
               "review2024": bool(z.review2024.any()) if len(z) else np.nan})
T = T.merge(pd.DataFrame(fs), on="sector", how="left")
T.to_csv(D / "ds1_crec_voice_test.csv", index=False)
for col in ["voice_2001_2017", "voice_pre"]:
    z = T[[col, "share_12"]].dropna()
    r, p = spearmanr(z[col], z.share_12)
    out.append(f"Test C Feinsektoren: Spearman {col} mit Anteil Listen 1+2: rho = {r:+.2f}, p = {p:.3f}, n = {len(z)}")
obs, p, k, n0 = perm_p(T.voice_2001_2017, T.review2024.fillna(False).astype(bool))
out.append(f"Test C Feinsektoren: voice_2001_2017 mit Erhoehung 2024 {T[T.review2024==True].voice_2001_2017.mean():.2f} "
           f"(n={k}), ohne {T[T.review2024!=True].voice_2001_2017.mean():.2f} (n={n0}); p = {p:.3f}")

# Gleiches auf Ebene der Warengruppen (verdraengte HS4-Gruppen aus population_weight.csv), Aufmerksamkeit der
# groben Sektorgruppe (crec_filter.SECT) 2001-2017; Standardfehler nach Gruppe geclustert.
CS = pd.DataFrame(rows_c)
w0 = CS[(CS.year >= 2001) & (CS.year <= 2017)].groupby("group").china_near.sum()
v = (1000 * w0 / econ[(econ.index >= 2001) & (econ.index <= 2017)].sum()).rename("voice_group")
H = pw[pw.data == "hs4"].copy()
H["group"] = [sector_of("hs4", c) for c in H.code]
H = H.merge(L[["hs4", "share_12", "review2024"]], left_on="code", right_on="hs4", how="left").merge(
    v, left_on="group", right_index=True, how="left").dropna(subset=["group", "share_12", "voice_group"])
H["review2024"] = H.review2024.fillna(False).astype(int)
H["l_voice"] = np.log1p(H.voice_group)
for f in ["share_12 ~ l_voice", "share_12 ~ l_voice + l_m_us + l_emp"]:
    m = smf.ols(f, H.dropna(subset=["l_m_us", "l_emp"])).fit(cov_type="cluster", cov_kwds={"groups": H.dropna(subset=["l_m_us", "l_emp"]).group})
    out.append(f"Test C HS4 (verdraengt, n={int(m.nobs)}, {H.group.nunique()} Gruppen): {f}: l_voice {m.params.l_voice:+.3f} "
               f"(p={m.pvalues.l_voice:.3f})" + (f"; l_m_us {m.params.l_m_us:+.3f} (p={m.pvalues.l_m_us:.3f})" if "l_m_us" in f else ""))
out.append("   Gruppenmittel: " + "; ".join(f"{gk} voice {gv.voice_group.iloc[0]:.1f}, Listen 1+2 {gv.share_12.mean():.2f}, 2024 {gv.review2024.mean():.2f}"
                                       for gk, gv in H.groupby("group")))
(D / "ds1_crec_voice_test.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
