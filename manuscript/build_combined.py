"""Builds the appendix as LaTeX (appendix_body.tex) for the combined manuscript.

main.tex inputs appendix_body.tex after the references. The Markdown source stays
manuscript/online_appendix.md; build_appendix.py still produces a separate PDF for submission.
Call: python3 manuscript/build_combined.py  (then latexmk -pdf main.tex)
"""
import re
import subprocess
from pathlib import Path

import build_appendix
from build_appendix import M, prepare

build_appendix.PAD = 6
build_appendix.CAP = 32  # narrower text block: cap long columns so short ones keep their words

md = prepare()
md = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)          # drop YAML header
md = md.replace("\n# References\n", "\n# References for the appendix {-}\n")
tmp = M / "appendix_build.md"
tmp.write_text(md)
tex = subprocess.run(["pandoc", str(tmp), "-f", "markdown", "-t", "latex", "--top-level-division=section"],
                     check=True, capture_output=True, text=True, cwd=M).stdout
tmp.unlink()
# headings: the letters are part of the text, so suppress LaTeX numbering
tex = re.sub(r"\\section\{([A-L])\. ", r"\\section*{Appendix \1. ", tex)
tex = re.sub(r"\\section\{", r"\\section*{", tex)
tex = re.sub(r"\\subsection\{", r"\\subsection*{", tex)
tex = re.sub(r"\\subsubsection\{", r"\\subsubsection*{", tex)
# appendix figures carry their own label text ("Figure E.1.")
tex = tex.replace("\\begin{figure}", "\\begin{figure}[htbp]").replace("\\caption{", "\\caption*{")
# tables: small type, hyphenation in narrow columns, captions kept with their table
tex = tex.replace("\\raggedright\\arraybackslash", "\\RaggedRight\\arraybackslash")
tex = re.sub(r"\\begin\{longtable\}", r"{\\footnotesize\\begin{longtable}", tex)
tex = tex.replace("\\end{longtable}", "\\end{longtable}}")
# table titles go inside the longtable, so title and head always share a page
tex = re.sub(r"\\textbf\{(Table [A-L]\.\d+\.[^{}]*)\}\n\n\{\\footnotesize\\begin\{longtable\}\[\]\{(.*?@\{\}\})\n",
             lambda m: "{\\footnotesize\\begin{longtable}[]{" + m.group(2) + "\n\\caption*{\\textbf{" + m.group(1) + "}}\\\\\n", tex, flags=re.S)
tex = re.sub(r"(?m)^(\\textbf\{(?:Figure|Table) [A-L]\.\d)", r"\\needspace{16\\baselineskip}\n\1", tex)
# figures keep their proportions and leave room for the caption
tex = tex.replace("height=\\textheight]", "height=0.62\\textheight,keepaspectratio]")
# file names in typewriter type: allow line breaks after / and _
tex = re.sub(r"\\texttt\{([^{}]*)\}", lambda m: "\\texttt{" + m.group(1).replace("/", "/\\allowbreak{}").replace("\\_", "\\_\\allowbreak{}") + "}", tex)
(M / "appendix_body.tex").write_text(tex)
print("appendix_body.tex written")
