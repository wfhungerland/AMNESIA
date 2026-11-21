"""Baut DS2 bis DS5 aus den Rohdaten in data/raw/.

Aufruf aus dem Repo-Wurzelordner: python3 data/build.py
Keine Interpolation, keine Glaettung: jede Zahl ist ein Wert der Quelle oder ein
einfacher Quotient aus Quellwerten (Formel jeweils in der Spaltenbeschreibung, data/README.md).
"""
import json
from pathlib import Path

import pandas as pd

D = Path(__file__).resolve().parent
RAW = D / "raw"
CASES = ["DEU", "JPN", "KOR", "CHN"]


def ds2_gdppc():
    """BIP pro Kopf (Maddison 2023, 2011-PPP-Dollar) und Verhaeltnis zu USA und GBR."""
    d = pd.read_stata(RAW / "maddison2023_web.dta")
    d = d[d.countrycode.isin(CASES + ["USA", "GBR"])]
    w = d.pivot(index="year", columns="countrycode", values="gdppc")
    rows = []
    for c in CASES + ["GBR"]:
        for y, v in w[c].dropna().items():
            us, gb = w.at[y, "USA"], w.at[y, "GBR"]
            rows.append({
                "country": c, "year": int(y), "gdppc_2011usd": round(float(v), 1),
                "ratio_usa": round(v / us, 4) if pd.notna(us) else None,
                "ratio_gbr": round(v / gb, 4) if pd.notna(gb) and c != "GBR" else None,
            })
    out = pd.DataFrame(rows).sort_values(["country", "year"])
    out.to_csv(D / "ds2_gdppc.csv", index=False)
    return out


def ds3_tfp():
    """TFP-Niveau relativ zu den USA (PWT 11.0, Variable ctfp, USA = 1 je Jahr)."""
    d = pd.read_stata(RAW / "pwt110.dta")
    d = d[d.countrycode.isin(CASES)][["countrycode", "year", "ctfp", "rtfpna"]].dropna(subset=["ctfp"])
    out = d.rename(columns={"countrycode": "country"})
    out["year"] = out.year.astype(int)
    out["ctfp"] = out.ctfp.astype(float).round(3)
    out["rtfpna"] = out.rtfpna.astype(float).round(3)
    out = out.sort_values(["country", "year"])
    out.to_csv(D / "ds3_tfp.csv", index=False)
    return out


def ds4_basic_research():
    """Grundlagenforschung: Anteil an GERD, Anteil am BIP; Sektoren GOV+HES gesondert."""
    t = pd.read_csv(RAW / "oecd_gerd_tord.csv")
    t = t[(t.UNIT_MEASURE == "XDC") & (t.PRICE_BASE == "V")]
    p = t.pivot_table(index=["REF_AREA", "TIME_PERIOD"], columns=["SECT_PERF", "TYPE_RD"],
                      values="OBS_VALUE", aggfunc="first")
    g = pd.read_csv(RAW / "oecd_msti_gerd_gdp.csv").set_index(["REF_AREA", "TIME_PERIOD"]).OBS_VALUE
    rows = []
    for (c, y), r in p.iterrows():
        tot = r.get(("_T", "_T"))
        br = r.get(("_T", "BR"))
        gh_br = r.get(("GOV", "BR"), float("nan")) + r.get(("HES", "BR"), float("nan"))
        gerd_gdp = g.get((c, y))
        share = br / tot if pd.notna(br) and pd.notna(tot) else None
        gh_share = gh_br / tot if pd.notna(gh_br) and pd.notna(tot) else None
        rows.append({
            "country": c, "year": int(y),
            "gerd_pct_gdp": round(gerd_gdp, 3) if pd.notna(gerd_gdp) else None,
            "br_share_gerd": round(share, 4) if share is not None else None,
            "br_pct_gdp": round(share * gerd_gdp, 3) if share is not None and pd.notna(gerd_gdp) else None,
            "br_gov_hes_pct_gdp": round(gh_share * gerd_gdp, 3) if gh_share is not None and pd.notna(gerd_gdp) else None,
        })
    out = pd.DataFrame(rows)
    out = out.dropna(subset=["br_share_gerd", "br_gov_hes_pct_gdp"], how="all").sort_values(["country", "year"])
    out.to_csv(D / "ds4_basic_research.csv", index=False)
    return out


def _wb(series):
    meta, rows = json.loads((RAW / f"wb_{series}.json").read_text())
    s = pd.DataFrame([(r["countryiso3code"], int(r["date"]), r["value"]) for r in rows],
                     columns=["country", "year", series])
    return s, meta.get("lastupdated")


def ds5_tbp():
    """Lizenzgebuehren (Weltbank WDI, BPM6 'charges for the use of IP'), laufende US-Dollar."""
    x, lu = _wb("BX.GSR.ROYL.CD")
    m, _ = _wb("BM.GSR.ROYL.CD")
    y, _ = _wb("NY.GDP.MKTP.CD")
    d = x.merge(m, on=["country", "year"]).merge(y, on=["country", "year"])
    d = d.dropna(subset=["BX.GSR.ROYL.CD", "BM.GSR.ROYL.CD"], how="all")
    out = pd.DataFrame({
        "country": d.country, "year": d.year,
        "receipts_usd_bn": (d["BX.GSR.ROYL.CD"] / 1e9).round(3),
        "payments_usd_bn": (d["BM.GSR.ROYL.CD"] / 1e9).round(3),
    })
    out["balance_usd_bn"] = (out.receipts_usd_bn - out.payments_usd_bn).round(3)
    out["coverage_ratio"] = (out.receipts_usd_bn / out.payments_usd_bn).round(3)
    out["balance_pct_gdp"] = ((d["BX.GSR.ROYL.CD"] - d["BM.GSR.ROYL.CD"]) / d["NY.GDP.MKTP.CD"] * 100).round(3)
    out["wb_lastupdated"] = lu
    out = out.sort_values(["country", "year"])
    out.to_csv(D / "ds5_tbp.csv", index=False)
    return out


def ds1_events():
    """Verbindet Reaktionen mit Meilensteinen: Phase (absorption/post) und Lag in Jahren."""
    m = pd.read_csv(D / "ds1_milestones.csv")
    r = pd.read_csv(D / "ds1_responses.csv")
    e = r.merge(m[["milestone_id", "sector", "year"]].rename(columns={"year": "milestone_year"}),
                left_on="sector_milestone", right_on="milestone_id", how="left").drop(columns="milestone_id")
    e["year"] = e.date.str[:4].astype(int)
    e["lag_years"] = e.year - e.milestone_year
    e["phase"] = e.lag_years.apply(lambda x: "absorption" if x < 0 else "post")
    e.to_csv(D / "ds1_events.csv", index=False)
    e.drop(columns=["mss_coder1"]).assign(mss_coder2="").to_csv(D / "ds1_coder2_blank.csv", index=False)
    return e


if __name__ == "__main__":
    for f in (ds1_events, ds2_gdppc, ds3_tfp, ds4_basic_research, ds5_tbp):
        o = f()
        print(f.__name__, len(o), "Zeilen")
