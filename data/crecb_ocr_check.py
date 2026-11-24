"""OCR-Pruefung des gebundenen Congressional Record: Anteil haeufiger englischer Funktionswoerter an allen
Wortzeichen auf den ersten fuenf Stichprobentagen (aus crecb_fetch.sample) der Jahre 1958, 1970 und 1985.
Ein stabiler Anteil spricht dafuer, dass das OCR-Rauschen ueber die Zeit nicht zunimmt.
Ergebnis: data/crecb_ocr_check.txt
"""
import gzip
import re
from pathlib import Path

import crecb_fetch as cf

D = Path(__file__).resolve().parent
FW = set("the of and to a in that is for it be this on as by with not are was have".split())
out = [f"Funktionswoerter ({len(FW)}): {' '.join(sorted(FW))}"]
for y in (1958, 1970, 1985):
    s = cf.sample(y)
    days = sorted(s)[:5]
    tok = fw = 0
    for d in days:
        for pkg, gid, _ in s[d]:
            cf.load(pkg, gid)
            p = cf.txt_path(gid)
            if not p.exists():
                continue
            w = re.findall(r"[a-z]+", gzip.decompress(p.read_bytes()).decode("utf-8", "ignore").lower())
            tok += len(w)
            fw += sum(1 for x in w if x in FW)
    out.append(f"{y}: Tage {', '.join(days)}; Woerter {tok:,}; Anteil Funktionswoerter {fw / tok:.3f}")
(D / "crecb_ocr_check.txt").write_text("\n".join(out) + "\n")
print("\n".join(out))
