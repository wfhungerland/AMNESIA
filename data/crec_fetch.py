"""Abruf des Congressional Record (govinfo, Collection CREC) 1995-2025 fuer die Kongressmessung China.

Schritt 1: alle Ausgaben (packages) je Jahr.
Schritt 2: alle Granules (Reden, Debattenabschnitte) je Ausgabe mit Titel und Klasse.
Schritt 3: Volltext (htm) laden fuer
  (a) alle Granules mit Wirtschaftstitel (Filter ECON in crec_salience.py) und
  (b) eine Pruefstichprobe: je Jahr 10 zufaellige Sitzungstage vollstaendig (Saat 1995),
      um zu messen, was der Titelfilter verfehlt.
Zwischenspeicher: data/raw/crec/ (lists/, granules/, htm/ als .htm.gz). Wiederholte Laeufe laden nichts neu.
Schluessel: api.data.gov, Header X-Api-Key. Der Netzwerk-Proxy setzt den echten Schluessel ein;
im Code steht nur ein Platzhalter (oder die Umgebungsvariable GOVINFO_KEY).

Aufruf aus dem Repo-Wurzelordner: python3 data/crec_fetch.py [lists|granules|htm|all]
"""
import gzip
import json
import os
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

D = Path(__file__).resolve().parent
sys.path.insert(0, str(D))
from crec_filter import is_econ  # noqa: E402

C = D / "raw" / "crec"
for sub in ("lists", "granules", "htm"):
    (C / sub).mkdir(parents=True, exist_ok=True)
API = "https://api.govinfo.gov"
KEY = os.environ.get("GOVINFO_KEY", "DUMMY")
YEARS = range(1995, 2026)
SAMPLE_DAYS = 10
RATE = 8.0  # Abrufe je Sekunde (Grenze laut Antwortkopf: 36.000 je Stunde = 10/s)

_lock = threading.Lock()
_next = [0.0]


def _wait():
    with _lock:
        now = time.time()
        t = max(now, _next[0])
        _next[0] = t + 1.0 / RATE
    time.sleep(max(0.0, t - now))


def fetch(url, tries=6):
    for i in range(tries):
        _wait()
        try:
            req = urllib.request.Request(url, headers={"X-Api-Key": KEY, "User-Agent": "research-client/1.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                rem = r.headers.get("X-Ratelimit-Remaining")
                if rem is not None and int(rem) < 300:
                    time.sleep(120)
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return b""
            time.sleep(60 if e.code == 429 else 2 ** i)
        except Exception:
            time.sleep(2 ** i)
    return None


def get_json(url, path):
    if path.exists():
        return json.loads(path.read_text())
    b = fetch(url)
    if b is None:
        return None
    d = json.loads(b) if b else {}
    path.write_text(json.dumps(d))
    return d


def packages(year):
    out, url = [], f"{API}/published/{year}-01-01/{year}-12-31?offsetMark=*&pageSize=1000&collection=CREC"
    p = C / "lists" / f"{year}.json"
    if p.exists():
        return json.loads(p.read_text())
    while url:
        b = fetch(url)
        d = json.loads(b)
        out += [x for x in d["packages"] if x["dateIssued"].startswith(str(year))]
        url = d.get("nextPage")
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


def htm_path(gid):
    return C / "htm" / f"{gid}.htm.gz"


def htm(pkg, gid):
    p = htm_path(gid)
    if p.exists():
        return
    b = fetch(f"{API}/packages/{pkg}/granules/{gid}/htm")
    if b is not None:
        p.write_bytes(gzip.compress(b))


def sample_packages(pk_by_year):
    rnd = random.Random(1995)
    return {y: sorted(rnd.sample(sorted(p["packageId"] for p in pk), min(SAMPLE_DAYS, len(pk))))
            for y, pk in pk_by_year.items()}


def skip(g):
    return g["granuleClass"] == "DAILYDIGEST" or g["granuleId"].endswith("FrontMatter")


def main(stage):
    pk = {y: packages(y) for y in YEARS}
    print("Ausgaben:", sum(len(v) for v in pk.values()), flush=True)
    if stage == "lists":
        return
    ids = [p["packageId"] for v in pk.values() for p in v]
    with ThreadPoolExecutor(16) as ex:
        gl = dict(zip(ids, ex.map(granules, ids)))
    print("Granules:", sum(len(v) for v in gl.values()), flush=True)
    if stage == "granules":
        return
    samp = {x for v in sample_packages(pk).values() for x in v}
    todo = []
    for pid, gs in gl.items():
        for g in gs:
            if skip(g):
                continue
            if is_econ(g["title"]) or pid in samp:
                todo.append((pid, g["granuleId"]))
    todo = [t for t in todo if not htm_path(t[1]).exists()]
    print("Volltexte offen:", len(todo), flush=True)
    done = [0]

    def job(t):
        htm(*t)
        done[0] += 1
        if done[0] % 2000 == 0:
            print("  geladen", done[0], flush=True)

    with ThreadPoolExecutor(16) as ex:
        list(ex.map(job, todo))
    print("fertig", flush=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "all")
