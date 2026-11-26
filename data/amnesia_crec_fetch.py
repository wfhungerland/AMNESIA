#!/usr/bin/env python3
"""
Trade-policy-amnesia counts from the US Congressional Record via the govinfo search API.

Endpoint
--------
POST https://api.govinfo.gov/search?api_key=DEMO_KEY
JSON body: {"query": <string>, "pageSize": <1..1000>, "offsetMark": "*"}
(the proxy injects the real key; DEMO_KEY is a placeholder). The response carries
"count" (total hits for the query), "offsetMark" (cursor for the next page) and
"results" (one record per granule, with packageId, granuleId, title, dateIssued,
download.txtLink, resultLink). Paging: resend the query with the returned offsetMark
until results come back empty.

Query syntax that works (Lucene-like, full text of the granule is indexed)
------------------------------------------------------------------------
  collection:CREC AND publishdate:range(1995-01-01,1995-12-31) AND (Japan OR Japanese)
  - collection restriction:   collection:CREC   or   collection:CRECB
  - date restriction:         publishdate:range(YYYY-MM-DD,YYYY-MM-DD)
  - boolean operators:        AND / OR in upper case, parentheses for grouping
  - phrase search:            "Alexander Hamilton" (double quotes inside the JSON string);
                              without quotes the words are ANDed (2005: 48 vs 90 hits)
  - "Smoot-Hawley" and "Smoot Hawley" return the same hits (hyphen is tokenised away).

Collections and units
---------------------
  CREC  (daily Congressional Record): 1994-2025 searchable; a granule is one article/speech
        section (e.g. CREC-1995-12-22-pt1-PgS19237-2). Counts = API "count" field (exact).
  CRECB (bound Congressional Record): searchable 1873-2018. For volumes up to 1998 the
        digitised granules are whole chamber-days ("Senate: June 21, 1955",
        "House of Representatives: ...", "Extensions of Remarks: ..."), granuleId
        GPO-CRECB-YYYY-ptN-N-N, plus a day-level parent (GPO-CRECB-YYYY-ptN-N) and a
        part-level package record (no granuleId). To avoid double counting, CRECB counts
        here are the number of DISTINCT CHAMBER-DAY granules (pattern GPO-CRECB-YYYY-ptN-N-N)
        among all paged results. From 1999 CRECB switches to article-level granules
        (CRECB-YYYY-ptN-PgN-N) that duplicate CREC, so CRECB is used for 1955-1998 only.
        CAUTION: a chamber-day granule is a whole day's proceedings, so co-occurrence in
        CRECB means "same chamber, same day", not "same speech"; CRECB and CREC counts are
        not comparable in level. 1994-1998 are fetched in both collections as a bridge.

Queries (Y = year, C = challenger)
---------------------------------
  base(Y)       = collection:<COLL> AND publishdate:range(Y-01-01,Y-12-31)
  C             = Japan: (Japan OR Japanese) | Korea: (Korea OR Korean) | China: (China OR Chinese)
  COMPLAINT     = (dumping OR "unfair trade" OR "trade deficit" OR "unfair competition"
                   OR "trade barriers")
  OWN_PROT      = ("Alexander Hamilton" OR "infant industry" OR "infant industries"
                   OR "American System" OR "Henry Clay" OR "McKinley tariff")
  SMOOT         = ("Smoot-Hawley" OR "Smoot Hawley")
  IMITATION     = ("Samuel Slater" OR "industrial espionage" OR "we copied" OR "pirated British")

  n_challenger     = base AND C
  n_complaint      = base AND C AND COMPLAINT                       (a)
  n_own_protection = base AND C AND COMPLAINT AND OWN_PROT          (b)
  n_smoot          = base AND C AND COMPLAINT AND SMOOT             (c)
  n_imitation      = base AND C AND COMPLAINT AND IMITATION         (d)

Outputs
-------
  amnesia_crec_counts.csv  columns: year, collection, challenger, n_challenger, n_complaint,
                           n_own_protection, n_smoot, n_imitation
  amnesia_crec_hits.json   granule records of (b), (c), (d) hits, for reading examples
Rate limit: ~1 request per second, retries with back-off on 429/5xx/network errors.
"""
import csv, json, os, re, sys, time
import requests

API = "https://api.govinfo.gov/search?api_key=DEMO_KEY"
OUT = os.path.dirname(os.path.abspath(__file__))
CHALL = {"Japan": "(Japan OR Japanese)", "Korea": "(Korea OR Korean)", "China": "(China OR Chinese)"}
COMPLAINT = '(dumping OR "unfair trade" OR "trade deficit" OR "unfair competition" OR "trade barriers")'
OWN_PROT = ('("Alexander Hamilton" OR "infant industry" OR "infant industries" OR "American System" '
            'OR "Henry Clay" OR "McKinley tariff")')
SMOOT = '("Smoot-Hawley" OR "Smoot Hawley")'
IMITATION = '("Samuel Slater" OR "industrial espionage" OR "we copied" OR "pirated British")'
PLAN = [("CRECB", y) for y in range(1955, 1999)] + [("CREC", y) for y in range(1994, 2026)]
CHAMBER_DAY = re.compile(r"^GPO-CRECB-\d{4}-pt\d+-\d+-\d+$")
S = requests.Session()


def post(query, page_size, mark="*"):
    for attempt in range(8):
        try:
            r = S.post(API, json={"query": query, "pageSize": page_size, "offsetMark": mark}, timeout=120)
            time.sleep(1.0)
            if r.status_code == 200:
                return r.json()
            print("HTTP", r.status_code, r.text[:200], file=sys.stderr)
        except Exception as e:  # network error
            print("ERR", e, file=sys.stderr)
        time.sleep(min(60, 2 ** attempt * 2))
    raise RuntimeError("failed: " + query)


def all_results(query):
    out, mark = [], "*"
    while True:
        d = post(query, 1000, mark)
        res = d.get("results") or []
        out += res
        nm = d.get("offsetMark")
        if not res or not nm or nm == mark:
            return out
        mark = nm


def count(coll, query, keep=False):
    """Return (n, records). CREC: API count field; CRECB: distinct chamber-day granules."""
    if coll == "CREC" and not keep:
        return post(query, 1).get("count", 0), []
    res = all_results(query)
    if coll == "CRECB":
        res = [r for r in res if r.get("granuleId") and CHAMBER_DAY.match(r["granuleId"])]
    uniq = {r.get("granuleId") or r["packageId"]: r for r in res}
    return len(uniq), list(uniq.values())


def main():
    cpath = os.path.join(OUT, "amnesia_crec_counts.csv")
    hpath = os.path.join(OUT, "amnesia_crec_hits.json")
    done, hits = set(), {}
    if os.path.exists(cpath):
        with open(cpath) as f:
            done = {(r["year"], r["collection"], r["challenger"]) for r in csv.DictReader(f)}
    if os.path.exists(hpath):
        hits = json.load(open(hpath))
    new = not os.path.exists(cpath)
    with open(cpath, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["year", "collection", "challenger", "n_challenger", "n_complaint",
                        "n_own_protection", "n_smoot", "n_imitation"])
        for coll, y in PLAN:
            base = f"collection:{coll} AND publishdate:range({y}-01-01,{y}-12-31)"
            for ch, cq in CHALL.items():
                if (str(y), coll, ch) in done:
                    continue
                a = f"{base} AND {cq} AND {COMPLAINT}"
                n_ch, _ = count(coll, f"{base} AND {cq}")
                n_a, _ = count(coll, a)
                row = [y, coll, ch, n_ch, n_a]
                for tag, extra in (("b", OWN_PROT), ("c", SMOOT), ("d", IMITATION)):
                    n, recs = count(coll, f"{a} AND {extra}", keep=True)
                    row.append(n)
                    hits[f"{coll}|{y}|{ch}|{tag}"] = [
                        {k: r.get(k) for k in ("granuleId", "packageId", "title", "dateIssued", "resultLink")}
                        | {"txtLink": (r.get("download") or {}).get("txtLink")} for r in recs]
                w.writerow(row); f.flush()
                json.dump(hits, open(hpath, "w"))
                print(row, flush=True)


if __name__ == "__main__":
    main()
