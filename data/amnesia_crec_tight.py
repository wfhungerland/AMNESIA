#!/usr/bin/env python3
"""
Tightened second pass, CREC (daily Congressional Record) only, 1994-2025.

Query (govinfo search API, POST https://api.govinfo.gov/search?api_key=DEMO_KEY,
body {"query": Q, "pageSize": 1000, "offsetMark": "*"}, paged with offsetMark):

  Q = collection:CREC AND publishdate:range(1994-01-01,2025-12-31)
      AND (Japan OR Japanese OR Korea OR Korean OR China OR Chinese)
      AND (dumping OR "unfair trade" OR "trade deficit" OR "unfair competition"
           OR "trade barriers" OR tariff OR tariffs)
      AND ("infant industry" OR "infant industries"
           OR ("Alexander Hamilton" AND (tariff OR tariffs OR protection OR manufactures))
           OR ("Henry Clay" AND (tariff OR tariffs OR "American System"))
           OR ("our own history" AND (tariff OR tariffs OR protection))
           OR ("when we were" AND (tariff OR tariffs OR protection OR "developing country")))

  Without the publishdate restriction the query returns 767 granules (19 are dated 2026);
  with it, 748. Denominator (challenger AND complaint, no memory terms), same date range:
    original five complaint terms                      -> 3,802 distinct granules
    five complaint terms + tariff OR tariffs (as in Q) -> 6,013 distinct granules

Note: all conditions are evaluated by the search engine at GRANULE level (a granule is one
CREC article; some are very long, e.g. omnibus statements or impeachment records).

Passage extraction (for manual coding):
  * every hit granule's text is downloaded (download.txtLink, an HTML <pre> file);
  * the text is split into speaker turns at lines of the form "  Mr./Mrs./Ms. NAME." or
    "  The PRESIDING OFFICER." etc.; a turn is treated as "the same speech";
  * each occurrence of an anchor phrase (infant industr*, Alexander Hamilton, Henry Clay,
    our own history, when we were) gives one passage: +-700 characters around the anchor,
    plus the speaker of the turn, and flags whether the turn names the challenger and
    whether trade/protection words occur within +-700 characters of the anchor.
  Output: amnesia_crec_tight_passages.json (scratch, for coding). The hand-coded results
  are in amnesia_crec_coded.csv (see the coding notes in the report).
"""
import html, json, os, re, sys, time
import requests

API = "https://api.govinfo.gov/search?api_key=DEMO_KEY"
CH = "(Japan OR Japanese OR Korea OR Korean OR China OR Chinese)"
CO = ('(dumping OR "unfair trade" OR "trade deficit" OR "unfair competition" OR "trade barriers" '
      'OR tariff OR tariffs)')
MEM = ('("infant industry" OR "infant industries" OR ("Alexander Hamilton" AND (tariff OR tariffs '
       'OR protection OR manufactures)) OR ("Henry Clay" AND (tariff OR tariffs OR "American System")) '
       'OR ("our own history" AND (tariff OR tariffs OR protection)) OR ("when we were" AND (tariff '
       'OR tariffs OR protection OR "developing country")))')
DATE = "publishdate:range(1994-01-01,2025-12-31)"
QUERY = f"collection:CREC AND {DATE} AND {CH} AND {CO} AND {MEM}"
DENOM = f"collection:CREC AND {DATE} AND {CH} AND {CO}"

ANCHORS = re.compile(r"infant industr\w*|Alexander Hamilton|Henry Clay|our own history|when we were", re.I)
CHALL = re.compile(r"\b(Japan|Japanese|Korea|Koreans?|China|Chinese)\b")
TRADE = re.compile(r"tariff|protection|protectionis|manufactur|infant industr|import|export|trade|duties|"
                   r"American System|developing country|industr", re.I)
TURN = re.compile(r"\n {2}((?:Mr|Mrs|Ms|Miss|Dr)\. [A-Z][A-Za-z'\-]*(?: [A-Z][A-Za-z'\-]+)*"
                  r"(?: of [A-Z][a-z]+(?: [A-Z][a-z]+)*)?|The (?:SPEAKER|PRESIDING OFFICER|"
                  r"CHAIRMAN|CHAIR|ACTING PRESIDENT|VICE PRESIDENT|PRESIDENT)[A-Za-z ()]*)\. ")
S = requests.Session()


def post(q, size, mark="*"):
    for a in range(8):
        try:
            r = S.post(API, json={"query": q, "pageSize": size, "offsetMark": mark}, timeout=120)
            time.sleep(1)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print("ERR", e, file=sys.stderr)
        time.sleep(2 ** a)
    raise RuntimeError(q)


def get(url):
    for a in range(8):
        try:
            r = S.get(url, timeout=300)
            time.sleep(1)
            if r.status_code == 200:
                return r.text
        except Exception as e:
            print("ERR", e, file=sys.stderr)
        time.sleep(2 ** a)
    raise RuntimeError(url)


def main(cache):
    os.makedirs(cache, exist_ok=True)
    out_dir = os.path.dirname(os.path.abspath(__file__))
    res, mark = [], "*"
    while True:
        d = post(QUERY, 1000, mark)
        res += d.get("results") or []
        if not d.get("results") or d.get("offsetMark") in (None, mark):
            break
        mark = d["offsetMark"]
    hits = {r["granuleId"]: r for r in res}
    print("hits", len(hits), "denominator", post(DENOM, 1).get("count"))
    passages = []
    for g, r in sorted(hits.items()):
        fp = os.path.join(cache, g + ".txt")
        if not os.path.exists(fp):
            raw = get(r["download"]["txtLink"] + "?api_key=DEMO_KEY")
            open(fp, "w").write(html.unescape(re.sub(r"<[^>]+>", "", raw)))
        t = open(fp).read()
        turns = [(m.start(), m.group(1)) for m in TURN.finditer(t)]
        for m in ANCHORS.finditer(t):
            i = m.start()
            prev = [x for x in turns if x[0] <= i]
            nxt = [x for x in turns if x[0] > i]
            s0 = prev[-1][0] if prev else 0
            s1 = nxt[0][0] if nxt else len(t)
            speaker = prev[-1][1] if prev else ""
            if not prev:  # Extensions of Remarks header "HON. NAME"
                h = re.search(r"HON\. ([A-Z][A-Z .\-']+)", t)
                speaker = ("HON. " + h.group(1).strip()) if h else ""
            win = t[max(0, i - 700): i + 700]
            passages.append({
                "granuleId": g, "packageId": r["packageId"], "title": r["title"],
                "date": r["dateIssued"], "anchor": m.group(0), "speaker": speaker,
                "chamber": {"S": "Senate", "H": "House", "E": "Extensions of Remarks", "D": "Daily Digest"}
                .get((re.search(r"-Pg([SHED])", g) or [None, "?"])[1], "?"),
                "challenger_in_turn": bool(CHALL.search(t[s0:s1])),
                "challenger_in_window": bool(CHALL.search(win)),
                "trade_in_window": bool(TRADE.search(win.replace(m.group(0), ""))),
                "window": re.sub(r"\s+", " ", win)})
    json.dump(passages, open(os.path.join(out_dir, "amnesia_crec_tight_passages.json"), "w"), indent=0)
    print("passages", len(passages))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "crec_tight_cache")
