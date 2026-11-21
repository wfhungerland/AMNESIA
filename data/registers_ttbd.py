"""Unabhaengige Ereignisliste (Panel-Revision 1): alle Antidumping- (AD) und Ausgleichszollverfahren (CVD)
der USA und der EU gegen Japan, Korea und China, 1980-2015, aus der Temporary Trade Barriers Database
(Bown; Weltbank). Zuordnung zu den DS1-Sektoren ueber HS-Codes der Verfahren. Phase gegen den
Sektor-Meilenstein (Hauptregel); Verfahren ohne passenden Sektor gegen den ersten Meilenstein des Falls.
Ergebnis: data/ds1_registers.csv (je Verfahren) und data/ds1_registers_summary.txt
"""
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent
R = D / "raw" / "ttbd"
files = [("AD", "US", R / "gad/GAD/GAD-USA.xls", "AD-USA"), ("AD", "EU", R / "gad/GAD/GAD-EUN.xls", "AD-EUN"),
         ("CVD", "US", R / "gcvd/GCVD/GCVD-USA.xls", "CVD-USA"), ("CVD", "EU", R / "gcvd/GCVD/GCVD-EUN.xls", "CVD-EUN")]
TARGET = {"JPN": "JP", "KOR": "KR", "CHN": "CN"}
# HS-Praefix -> DS1-Meilenstein, nach Fall
SECT = {"JP": [("8542", "M-JP-DRAM"), ("8541", "M-JP-SEMI"), ("8703", "M-JP-AUTO"), ("72", "M-JP-STEEL"), ("73", "M-JP-STEEL"),
               ("8528", "M-JP-TV"), ("52", "M-JP-TEXT")],
        "KR": [("8542", "M-KR-DRAM"), ("8901", "M-KR-SHIP")],
        "CN": [("854140", "M-CN-SOLAR"), ("8541", "M-CN-SOLAR"), ("8517", "M-CN-TEL"), ("870380", "M-CN-EV")]}
FIRST = {"JP": "M-JP-TEXT", "KR": "M-KR-DRAM", "CN": "M-CN-MFG"}
m = pd.read_csv(D / "ds1_milestones.csv").set_index("milestone_id")
rows = []
for kind, inc, f, pre in files:
    x = pd.read_excel(f, sheet_name=None)
    master = next(v for k, v in x.items() if k.endswith("Master"))
    prods = next((v for k, v in x.items() if k.endswith("Products")), pd.DataFrame(columns=["CASE_ID", "HS_CODE"]))
    cty = next(c for c in master.columns if c.endswith("CTY_CODE") and c.startswith("INV") is False) if False else "INV_CTY_CODE"
    mm = master[master[cty].isin(TARGET)].copy()
    hs = prods.groupby("CASE_ID").HS_CODE.apply(lambda s: [str(v).split(".")[0] for v in s.dropna()])
    for _, r in mm.iterrows():
        case = TARGET[r[cty]]
        codes = hs.get(r.CASE_ID, [])
        ms = None
        for prefix, mid in SECT[case]:
            if any(c.startswith(prefix) for c in codes):
                ms = mid; break
        sector_matched = ms is not None
        ms = ms or FIRST[case]
        init = pd.to_datetime(r.INIT_DATE, errors="coerce")
        fin = str(r["F_AD_MEASURE"] if "F_AD_MEASURE" in r.index else r["F_CVD_MEASURE"]).strip().upper()
        rows.append({"kind": kind, "incumbent": inc, "case": case, "case_id": r.CASE_ID, "product": r.PRODUCT,
                     "init_year": init.year if pd.notna(init) else None, "final_measure": fin not in (".", "MI", "NAN", ""),  # AVD, SD, SA, PU: endgueltige Massnahme in Kraft
                     "milestone": ms, "sector_matched": sector_matched, "milestone_year": int(m.loc[ms, "year"])})
d = pd.DataFrame(rows).dropna(subset=["init_year"])
d["init_year"] = d.init_year.astype(int)
d["lag"] = d.init_year - d.milestone_year
d["phase"] = d.lag.apply(lambda v: "absorption" if v < 0 else "post")
d.to_csv(D / "ds1_registers.csv", index=False)
out = [f"Verfahren gesamt: {len(d)} ({d.init_year.min()}-{d.init_year.max()})"]
for case in ["JP", "KR", "CN"]:
    z = d[d.case == case]
    out.append(f"{case}: {len(z)} Verfahren; vor Meilenstein {int((z.phase=='absorption').sum())}, danach {int((z.phase=='post').sum())}; "
               f"endgueltige Massnahme vor {int(((z.phase=='absorption')&z.final_measure).sum())}, danach {int(((z.phase=='post')&z.final_measure).sum())}; "
               f"sektorgenau zugeordnet {int(z.sector_matched.sum())}")
    zs = z[z.sector_matched]
    for ms, g in zs.groupby("milestone"):
        out.append(f"   {ms} ({int(g.milestone_year.iloc[0])}): vor {int((g.phase=='absorption').sum())}, danach {int((g.phase=='post').sum())}")
(D / "ds1_registers_summary.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out))
