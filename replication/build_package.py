"""Builds the anonymised replication package as dist/replication_package.zip.

Call from the repository root: python3 replication/build_package.py
Includes derived data, scripts, checksums, figure scripts and the appendix source;
excludes raw data, caches and internal working files. Stops if identifying strings are found.
"""
import csv
import io
import re
import zipfile
from pathlib import Path

R = Path(__file__).resolve().parent.parent
OUT = R / "dist" / "replication_package.zip"
EXCLUDE = {"data/ds1_coder2_chat.csv"}  # informal, non-blind coding notes
DROP_COLS = {"data/ds1_milestones.csv": {"source_in_repo"}}  # paths to internal working notes
FORBIDDEN = re.compile(r"hungerland|gmail|bmwe|stanford|dropbox|/home/|wfhungerland|claude-session", re.I)


def files():
    for p in sorted((R / "data").glob("*")):
        if p.is_file() and p.suffix in {".csv", ".txt", ".md", ".py", ".sh"}:
            yield p
    yield R / "data" / "raw" / "SHA256SUMS.abruf"
    for p in sorted((R / "manuscript" / "figures").glob("*.py")):
        yield p
    yield R / "manuscript" / "build_appendix.py"
    yield R / "manuscript" / "online_appendix.md"


def main():
    OUT.parent.mkdir(exist_ok=True)
    hits = []
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(R / "replication" / "README.md", "README.md")
        z.write(R / "replication" / "requirements.txt", "requirements.txt")
        n = 2
        for p in files():
            rel = p.relative_to(R).as_posix()
            if rel in EXCLUDE:
                continue
            text = p.read_text(errors="ignore")
            if rel in DROP_COLS:
                rows = list(csv.DictReader(io.StringIO(text)))
                keep = [c for c in rows[0] if c not in DROP_COLS[rel]]
                buf = io.StringIO()
                w = csv.DictWriter(buf, keep, extrasaction="ignore", lineterminator="\n")
                w.writeheader(); w.writerows(rows)
                text = buf.getvalue()
            for m in FORBIDDEN.finditer(text):
                hits.append(f"{rel}: {m.group(0)}")
            z.writestr(rel, text) if rel in DROP_COLS else z.write(p, rel)
            n += 1
    if hits:
        OUT.unlink()
        raise SystemExit("identifying strings found:\n" + "\n".join(hits[:40]))
    print(f"{OUT.relative_to(R)}: {n} files, {OUT.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
