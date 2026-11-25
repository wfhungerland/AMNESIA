"""Builds the appendix as LaTeX (appendix_body.tex) for the combined manuscript.

main.tex inputs appendix_body.tex after the references. The Markdown source stays
manuscript/online_appendix.md; build_appendix.py still produces a separate PDF for submission.
Call: python3 manuscript/build_combined.py  (then latexmk -pdf main.tex)
"""
import re
import subprocess
from pathlib import Path

from build_appendix import M, prepare

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
(M / "appendix_body.tex").write_text(tex)
print("appendix_body.tex written")
