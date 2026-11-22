"""Stichprobe aus dem gebundenen Congressional Record (govinfo, Collection CRECB) 1955-1994 fuer den Fall Japan.

Der gebundene Record liegt je Band (package) und je Sitzungstag und Kammer (granule) nur als PDF mit
Textschicht vor, ohne Debattentitel. Deshalb: je Jahr 20 zufaellige Sitzungstage (Saat 1960), alle
Kammer-Granules dieser Tage (House, Senate, Extensions of Remarks), Text mit pdftotext auslesen.
Das PDF wird danach geloescht; gespeichert wird nur der Text (data/raw/crecb/txt/*.txt.gz).
Schluessel wie crec_fetch.py (Header X-Api-Key, Platzhalter; der Proxy setzt den echten Schluessel ein).

Aufruf aus dem Repo-Wurzelordner: python3 data/crecb_fetch.py [erstes_jahr] [letztes_jahr]
"""
import gzip
import json
import random
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import crec_fetch  # noqa: E402
from crec_fetch import API, fetch  # noqa: E402

crec_fetch.RATE = 2.0  # laeuft neben crec_fetch.py; gemeinsame Grenze 10 Abrufe je Sekunde

C = D / "raw" / "crecb"
for sub in ("lists", "granules", "txt"):
    (C / sub).mkdir(parents=True, exist_ok=True)
DAYS = 20


def packages(year):
    p = C / "lists" / f"{year}.json"
    if p.exists():
        return json.loads(p.read_text())
    out, url = [], f"{API}/published/{year}-01-01/{year + 3}-12-31?offsetMark=*&pageSize=1000&collection=CRECB"
    while url:
        d = json.loads(fetch(url))
        out += [x for x in d["packages"] if x["packageId"].startswith(f"GPO-CRECB-{year}-")]
        url = d.get("nextPage")
    out = list({x["packageId"]: x for x in out}.values())
    p.write_text(json.dumps(out))
    return out


def granules(pkg):
    p = C / "granules" / f"{pkg}.json"
    if p.exists():
        return json.loads(p.read_text())
    out, url = [], f"{API}/packages/{pkg}/granules?offsetMark=*&pageSize=1000"
    while url:
        b = fetch(url)
        if not b:
            break
        d = json.loads(b)
        out += d.get("granules", [])
        url = d.get("nextPage")
    p.write_text(json.dumps(out))
    return out


def chamber_granules(year):
    """Kammer-Granules (Titel 'Kammer: Datum') des Jahres, nach Datum."""
    by_day = {}
    for pk in packages(year):
        for g in granules(pk["packageId"]):
            m = re.match(r"^(House of Representatives|Senate|Extensions of Remarks)\s*:\s*(.+)$", g["title"])
            if m:
                by_day.setdefault(m.group(2).strip(), []).append((pk["packageId"], g["granuleId"], m.group(1)))
    return by_day


def sample(year):
    by_day = chamber_granules(year)
    rnd = random.Random(1960 + year)
    days = sorted(by_day)
    pick = sorted(rnd.sample(days, min(DAYS, len(days))))
    return {d: by_day[d] for d in pick}


def txt_path(gid):
    return C / "txt" / f"{gid}.txt.gz"


def load(pkg, gid):
    p = txt_path(gid)
    if p.exists():
        return
    b = fetch(f"{API}/packages/{pkg}/granules/{gid}/pdf")
    if not b:
        return
    with tempfile.TemporaryDirectory() as td:
        f = Path(td) / "g.pdf"
        f.write_bytes(b)
        r = subprocess.run(["pdftotext", str(f), "-"], capture_output=True)
    p.write_bytes(gzip.compress(r.stdout))


def main(a=1960, b=1994):
    todo = []
    for y in range(a, b + 1):
        s = sample(y)
        todo += [(pkg, gid) for v in s.values() for pkg, gid, _ in v]
        print(y, "Tage", len(s), "Granules", sum(len(v) for v in s.values()), flush=True)
    todo = [t for t in todo if not txt_path(t[1]).exists()]
    print("PDF offen:", len(todo), flush=True)
    n = [0]

    def job(t):
        load(*t)
        n[0] += 1
        if n[0] % 100 == 0:
            print("  geladen", n[0], flush=True)

    with ThreadPoolExecutor(12) as ex:
        list(ex.map(job, todo))
    print("fertig", flush=True)


if __name__ == "__main__":
    main(*(int(x) for x in sys.argv[1:3]))
