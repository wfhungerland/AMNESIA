"""Online Appendix: fuegt die Reaktionstabellen aus data/ds1_events.csv ein und setzt das PDF mit pandoc.

Aufruf: python3 manuscript/build_appendix.py  (Ausgabe manuscript/online_appendix.pdf)
"""
from pathlib import Path
import subprocess
import pandas as pd

M = Path(__file__).resolve().parent
R = M.parent
e = pd.read_csv(R / "data" / "ds1_events.csv")
NAMES = {"DE": "Germany against Britain", "JP": "Japan against the United States",
         "KR": "Korea against the United States and Japan", "CN": "China against the United States and the EU"}


def src(s):
    return (s.replace("; Policy Amnesia Index v2.5", "").replace("Policy Amnesia Index v2.5", "project source file")
             .replace("Birmingham speech", "Birmingham speech, 15 May 1903"))


def table(sub):
    rows = ["| ID | Year | Response | Sector (milestone) | Lag | IR | Phase | Source |", "|---|---|---|---|---|---|---|---|"]
    for r in sub.sort_values(["year", "response_id"]).itertuples():
        rows.append(f"| {r.response_id.replace('-', '\u2011')} | {r.year} | {r.description.replace('|', '/')} | {r.sector} ({r.milestone_year}) "
                    f"| {r.lag_years} | {r.reach_coder1} | {'before' if r.phase == 'absorption' else 'after'} | {src(r.source_original)} |")
    return "\n".join(rows)


c1 = "\n\n".join(f"*{NAMES[c]}*\n\n{table(e[e.case == c])}" for c in ["DE", "JP", "KR", "CN"])
g5 = table(e[e.case == "JPGB"])
md = (M / "online_appendix.md").read_text().replace("{{C1}}", c1).replace("{{G5}}", g5)


def widths(text):
    """Setzt die Strichzahl der Trennzeile jeder Pipe-Tabelle proportional zur Textlaenge der Spalten (pandoc liest daraus die Spaltenbreiten)."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("|---") and i > 0 and lines[i - 1].startswith("|"):
            block = [lines[i - 1]]
            j = i + 1
            while j < len(lines) and lines[j].startswith("|"):
                block.append(lines[j]); j += 1
            cells = [[c.strip() for c in b.strip().strip("|").split("|")] for b in block]
            n = len(cells[0])
            col = [[r[k] if k < len(r) else "" for r in cells] for k in range(n)]
            w = [max(min(max(len(c) for c in cs), 60), max(len(t) for c in cs for t in (c.split() or [""])) + 3, 4) for cs in col]
            lines[i] = "|" + "|".join("-" * x for x in w) + "|"
    return "\n".join(lines)


md = widths(md)
tmp = M / "online_appendix_build.md"
tmp.write_text(md)
header = M / "online_appendix_header.tex"
header.write_text(r"""\usepackage{etoolbox}
\AtBeginEnvironment{longtable}{\footnotesize}
\usepackage{caption}
\captionsetup{font=small}
\captionsetup[figure]{labelformat=empty}
\usepackage{newunicodechar}
\newunicodechar{≥}{\ensuremath{\geq}}
\newunicodechar{≤}{\ensuremath{\leq}}
\newunicodechar{−}{\ensuremath{-}}
\newunicodechar{λ}{\ensuremath{\lambda}}
\newunicodechar{ρ}{\ensuremath{\rho}}
\newunicodechar{×}{\ensuremath{\times}}
\newunicodechar{α}{\ensuremath{\alpha}}
\newunicodechar{‑}{\mbox{-}}
\setlength{\emergencystretch}{3em}
""")
subprocess.run(["pandoc", str(tmp), "-o", str(M / "online_appendix.pdf"), "--pdf-engine=pdflatex",
                "-V", "geometry:margin=2.2cm", "-V", "fontsize=11pt", "-V", "documentclass=article",
                "-V", "colorlinks=false", "-V", "lang=en-GB", "--toc", "-H", str(header),
                "--resource-path", str(M)], check=True, cwd=M)
tmp.unlink(); header.unlink()
