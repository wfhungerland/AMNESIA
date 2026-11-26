"""Builds the blind sheet for the independent second coding of the reach score (IR 1-5).

The coder sees only what the measure is: incumbent, target, short description, legal basis or source. Milestones,
lags, phases, response types and the first coder's scores are withheld, and items are shuffled.
Items: the 48 responses of ds1_events.csv (incl. Japan against Britain) and the 42 entries of broad_register.csv.
Output: data/coder2/coding_sheet.xlsx (to hand out), data/coder2/key.csv (not to hand out).
"""
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

D = Path(__file__).resolve().parent
O = D / "coder2"
O.mkdir(exist_ok=True)
NAME = {"GB": "United Kingdom", "US": "United States", "EU": "European Union", "JP": "Japan", "KR": "Korea", "CN": "China",
        "DE": "Germany", "TW": "Taiwan", "HK": "Hong Kong", "BR": "Brazil", "MX": "Mexico", "TH": "Thailand", "MY": "Malaysia",
        "VN": "Vietnam", "FR": "France", "IN": "India"}
CH = {"DE": "Germany", "JP": "Japan", "KR": "Korea", "CN": "China", "JPGB": "Japan"}
e = pd.read_csv(D / "ds1_events.csv")
r = pd.read_csv(D / "broad_register.csv", dtype=str)


def names(s):
    return "; ".join(NAME.get(x, x) for x in str(s).replace(",", ";").replace("+", ";").split(";") if x and x != "nan")


items = [{"orig_id": x.response_id, "set": "responses", "incumbent": names(x.incumbent), "target": CH[x.case],
          "measure": x.description, "legal_basis_or_source": x.source_original, "coder1": int(x.reach_coder1)} for x in e.itertuples()]
items += [{"orig_id": x.instrument_id, "set": "register", "incumbent": "United States", "target": names(x.target),
           "measure": x.instrument, "legal_basis_or_source": x.legal_basis, "coder1": int(x.reach)} for x in r.itertuples()]
import re
for it in items:  # no hint of the first coder's scores, English only
    for k in ("measure", "legal_basis_or_source"):
        it[k] = re.sub(r"\s*=\s*IR\s*\d", "", str(it[k])).replace("Originalfassung", "original version").replace("; first agreements entered as B-37 to B-42", "")
K = pd.DataFrame(items).sample(frac=1, random_state=20261125).reset_index(drop=True)
K.insert(0, "item", [f"C{i + 1:02d}" for i in range(len(K))])
K.to_csv(O / "key.csv", index=False)

wb = Workbook()
ws = wb.active
ws.title = "coding"
cols = ["item", "incumbent", "target", "measure", "legal_basis_or_source", "IR (1-5)", "doubt (tick if two levels seemed possible)", "note"]
ws.append(cols)
for x in K.itertuples():
    ws.append([x.item, x.incumbent, x.target, x.measure, x.legal_basis_or_source, None, None, None])
for c, w in zip("ABCDEFGH", [7, 16, 14, 60, 40, 9, 14, 40]):
    ws.column_dimensions[c].width = w
for cell in ws[1]:
    cell.font = Font(bold=True)
    cell.fill = PatternFill("solid", fgColor="E8EEF6")
    cell.alignment = Alignment(wrap_text=True, vertical="top")
for row in ws.iter_rows(min_row=2):
    for cell in row:
        cell.alignment = Alignment(wrap_text=True, vertical="top")
ws.freeze_panes = "B2"
dv = DataValidation(type="whole", operator="between", formula1="1", formula2="5", allow_blank=True,
                    error="Enter a whole number from 1 to 5.", errorTitle="IR score")
ws.add_data_validation(dv)
dv.add(f"F2:F{len(K) + 1}")
rules = wb.create_sheet("rules")
for line in (O / "CODING_RULES.md").read_text().splitlines():
    rules.append([line])
rules.column_dimensions["A"].width = 120
wb.save(O / "coding_sheet.xlsx")
print(f"{len(K)} items written: {K.set.value_counts().to_dict()}")
