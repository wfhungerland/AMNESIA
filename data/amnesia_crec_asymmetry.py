#!/usr/bin/env python3
"""
Asymmetry and benchmark extension of the CREC amnesia test (see amnesia_crec_tight.py).

Source: govinfo search API, POST https://api.govinfo.gov/search?api_key=DEMO_KEY (the proxy injects
the real key), body {"query": Q, "pageSize": 1000, "offsetMark": "*"}, paged with offsetMark.
Collection CREC only. One query per calendar year Y = 1994..2025, i.e. every query below is prefixed
with

  collection:CREC AND publishdate:range(Y-01-01,Y-12-31) AND ...

The unit is the distinct granule (granuleId); all granule ids are collected per year and pooled
(set union) over years. All conditions are evaluated by the search engine at granule level.

Building blocks
  CH  = (Japan OR Japanese OR Korea OR Korean OR China OR Chinese)
  CO  = (dumping OR "unfair trade" OR "trade deficit" OR "unfair competition" OR "trade barriers"
         OR tariff OR tariffs)
  AL  = (Canada OR Canadian OR "European Union" OR Germany OR German OR France OR French)
  MEM = ("infant industry" OR "infant industries"
         OR ("Alexander Hamilton" AND (tariff OR tariffs OR protection OR manufactures))
         OR ("Henry Clay" AND (tariff OR tariffs OR "American System"))
         OR ("our own history" AND (tariff OR tariffs OR protection))
         OR ("when we were" AND (tariff OR tariffs OR protection OR "developing country")))
  Attack categories (policies the US itself once used):
  SUB = (subsidy OR subsidies OR subsidized OR subsidised)
  PRO = ("protectionism" OR "protectionist" OR "closed market" OR "market access")
  IPR = ("intellectual property" OR piracy OR counterfeit
         OR (theft AND (intellectual OR technology OR "trade secret" OR "trade secrets"))
         OR "forced technology transfer" OR "technology transfer")
  IND = ("industrial policy" OR "infant industry" OR "infant industries" OR "state-owned")
  ANY = (SUB OR PRO OR IPR OR IND)

Sets and measures (each row of amnesia_crec_asymmetry.csv: year, set, measure, count)
  set A (challenger)          : A   = CH AND CO
  set B (allies, no catch-up) : B   = AL AND CO AND NOT CH
  measure "all"               : the set itself
  measure "memory"            : set AND MEM
  measures "subsidies", "protection", "ip_imitation", "industrial_policy": set AND SUB / PRO / IPR / IND
  measure "any_attack"        : set AND ANY (queried directly; also checked against the union of the four)
  measure "any_attack_no_memory": (set AND ANY) minus (set AND MEM), computed from the id sets
  year = "1994-2025" rows are pooled distinct granules.

Note: "infant industry/industries" is both an attack term (IND) and a memory anchor (MEM); IND
therefore overlaps MEM by construction. Words are matched by the search engine, which may apply
stemming.

Benchmark coding: 30 random hits of B AND MEM (random.seed(2026), sampled from the sorted pooled id
list) are downloaded (download.txtLink) and split into passages with the same anchor/speaker-turn
rules as amnesia_crec_tight.py (+-700 characters around each anchor; turn = speaker turn; flags
whether an ally (AL terms) is named in the same turn). Passages: amnesia_crec_benchmark_passages.json
(scratch). They were read and coded by hand with the rules of amnesia_crec_code.py
(uses_own_history = yes only if the speaker invokes the US's own past protection / industrial
policy / tariff history; purpose in justify_protection_now, argue_against_protection,
excuse_or_understand_challenger, other); codes are in CODES below and written to
amnesia_crec_benchmark_coded.csv by `python3 amnesia_crec_asymmetry.py code`.

Usage: python3 amnesia_crec_asymmetry.py fetch [cache]   # counts + sample passages
       python3 amnesia_crec_asymmetry.py code            # write benchmark coded csv
"""
import csv, html, json, os, random, re, sys, time
import requests

API = "https://api.govinfo.gov/search?api_key=DEMO_KEY"
CH = "(Japan OR Japanese OR Korea OR Korean OR China OR Chinese)"
CO = ('(dumping OR "unfair trade" OR "trade deficit" OR "unfair competition" OR "trade barriers" '
      'OR tariff OR tariffs)')
AL = '(Canada OR Canadian OR "European Union" OR Germany OR German OR France OR French)'
MEM = ('("infant industry" OR "infant industries" OR ("Alexander Hamilton" AND (tariff OR tariffs '
       'OR protection OR manufactures)) OR ("Henry Clay" AND (tariff OR tariffs OR "American System")) '
       'OR ("our own history" AND (tariff OR tariffs OR protection)) OR ("when we were" AND (tariff '
       'OR tariffs OR protection OR "developing country")))')
CATS = {
    "subsidies": '(subsidy OR subsidies OR subsidized OR subsidised)',
    "protection": '("protectionism" OR "protectionist" OR "closed market" OR "market access")',
    "ip_imitation": ('("intellectual property" OR piracy OR counterfeit OR (theft AND (intellectual OR '
                     'technology OR "trade secret" OR "trade secrets")) OR "forced technology transfer" '
                     'OR "technology transfer")'),
    "industrial_policy": '("industrial policy" OR "infant industry" OR "infant industries" OR "state-owned")',
}
ANY = "(" + " OR ".join(CATS.values()) + ")"
SETS = {"A": f"{CH} AND {CO}", "B": f"{AL} AND {CO} AND NOT {CH}"}
MEASURES = {"all": None, "memory": MEM, **CATS, "any_attack": ANY}
YEARS = range(1994, 2026)
HERE = os.path.dirname(os.path.abspath(__file__))
S = requests.Session()


def post(q, size=1000, mark="*"):
    for a in range(8):
        try:
            r = S.post(API, json={"query": q, "pageSize": size, "offsetMark": mark}, timeout=180)
            time.sleep(1)
            if r.status_code == 200:
                return r.json()
            print("HTTP", r.status_code, r.text[:200], file=sys.stderr)
        except Exception as e:
            print("ERR", e, file=sys.stderr)
        time.sleep(2 ** a)
    raise RuntimeError(q)


def ids(q):
    out, mark = {}, "*"
    while True:
        d = post(q, 1000, mark)
        for r in d.get("results") or []:
            out[r["granuleId"]] = r
        if not d.get("results") or d.get("offsetMark") in (None, mark):
            return out
        mark = d["offsetMark"]


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


ANCHORS = re.compile(r"infant\s+industr\w*|Alexander\s+Hamilton|Henry\s+Clay|our\s+own\s+history|when\s+we\s+were", re.I)
ALLY = re.compile(r"\b(Canada|Canadian|European Union|Germany|German|France|French)\b")
TRADE = re.compile(r"tariff|protection|protectionis|manufactur|infant industr|import|export|trade|duties|"
                   r"American System|developing country|industr", re.I)
TURN = re.compile(r"\n {2}((?:Mr|Mrs|Ms|Miss|Dr)\. [A-Z][A-Za-z'\-]*(?: [A-Z][A-Za-z'\-]+)*"
                  r"(?: of [A-Z][a-z]+(?: [A-Z][a-z]+)*)?|The (?:SPEAKER|PRESIDING OFFICER|"
                  r"CHAIRMAN|CHAIR|ACTING PRESIDENT|VICE PRESIDENT|PRESIDENT)[A-Za-z ()]*)\. ")


def fetch(cache):
    os.makedirs(cache, exist_ok=True)
    pooled = {(s, m): {} for s in SETS for m in MEASURES}
    rows = []
    for y in YEARS:
        D = f"collection:CREC AND publishdate:range({y}-01-01,{y}-12-31)"
        for s, sq in SETS.items():
            for m, mq in MEASURES.items():
                q = f"{D} AND {sq}" + (f" AND {mq}" if mq else "")
                got = ids(q)
                pooled[(s, m)].update(got)
                rows.append((y, s, m, len(got)))
            yr = {m: {g for g, r in pooled[(s, m)].items() if r["dateIssued"][:4] == str(y)} for m in MEASURES}
            un = set().union(*(yr[c] for c in CATS))
            if un != yr["any_attack"]:
                print("WARN union != any", y, s, len(un), len(yr["any_attack"]), file=sys.stderr)
            rows.append((y, s, "any_attack_no_memory", len(yr["any_attack"] - yr["memory"])))
            print(y, s, {m: len(yr[m]) for m in MEASURES}, flush=True)
    for s in SETS:
        for m in MEASURES:
            rows.append(("1994-2025", s, m, len(pooled[(s, m)])))
        rows.append(("1994-2025", s, "any_attack_no_memory",
                     len(set(pooled[(s, "any_attack")]) - set(pooled[(s, "memory")]))))
    with open(os.path.join(HERE, "amnesia_crec_asymmetry.csv"), "w", newline="") as f:
        w = csv.writer(f); w.writerow(["year", "set", "measure", "count"]); w.writerows(rows)
    json.dump({f"{s}|{m}": sorted(v) for (s, m), v in pooled.items() if m != "all"},
              open(os.path.join(cache, "asymmetry_ids.json"), "w"))
    # benchmark sample: 30 random hits of B AND MEM
    bm = pooled[("B", "memory")]
    random.seed(2026)
    samp = random.sample(sorted(bm), 30)
    passages = []
    for g in samp:
        r = bm[g]
        fp = os.path.join(cache, g + ".txt")
        if not os.path.exists(fp):
            raw = get(r["download"]["txtLink"] + "?api_key=DEMO_KEY")
            open(fp, "w").write(html.unescape(re.sub(r"<[^>]+>", "", raw)))
        t = open(fp).read()
        turns = [(mm.start(), mm.group(1)) for mm in TURN.finditer(t)]
        for mm in ANCHORS.finditer(t):
            i = mm.start()
            prev = [x for x in turns if x[0] <= i]
            nxt = [x for x in turns if x[0] > i]
            s0 = prev[-1][0] if prev else 0
            s1 = nxt[0][0] if nxt else len(t)
            speaker = prev[-1][1] if prev else ""
            if not prev:
                h = re.search(r"HON\. ([A-Z][A-Z .\-']+)", t)
                speaker = ("HON. " + h.group(1).strip()) if h else ""
            win = t[max(0, i - 700): i + 700]
            passages.append({
                "granuleId": g, "packageId": r["packageId"], "title": r["title"], "date": r["dateIssued"],
                "anchor": re.sub(r"\s+", " ", mm.group(0)), "speaker": speaker,
                "chamber": {"S": "Senate", "H": "House", "E": "Extensions of Remarks", "D": "Daily Digest"}
                .get((re.search(r"-Pg([SHED])", g) or [None, "?"])[1], "?"),
                "ally_in_turn": bool(ALLY.search(t[s0:s1])),
                "trade_in_window": bool(TRADE.search(win.replace(mm.group(0), ""))),
                "window": re.sub(r"\s+", " ", win)})
    json.dump({"sample": samp, "passages": passages},
              open(os.path.join(HERE, "amnesia_crec_benchmark_passages.json"), "w"), indent=0)
    print("B memory hits", len(bm), "sample", len(samp), "passages", len(passages))


# Hand codes for the 30 sampled B AND MEM granules (filled after reading the passages):
# granule -> (speaker, uses_own_history, purpose, ally_in_same_speech, quote, note)
CODES = {}


def code():
    d = json.load(open(os.path.join(HERE, "amnesia_crec_benchmark_passages.json")))
    by = {}
    for p in d["passages"]:
        by.setdefault(p["granuleId"], []).append(p)
    rows = []
    for g in sorted(d["sample"]):
        ps = by.get(g, [])
        sp, yes, pur, al, q, note = CODES[g]
        p0 = ps[0] if ps else {}
        rows.append(dict(granule_id=g, year=int(g[5:9]), chamber=p0.get("chamber", ""), speaker=sp,
                         uses_own_history=yes, purpose=pur, ally_in_same_speech=al,
                         stratum="random30_of_B_memory", quote=q, note=note,
                         title=(p0.get("title") or "")[:120],
                         url=f"https://www.govinfo.gov/app/details/{g.split('-pt')[0]}/{g}"))
    cols = ["granule_id", "year", "chamber", "speaker", "uses_own_history", "purpose", "ally_in_same_speech",
            "stratum", "quote", "note", "title", "url"]
    with open(os.path.join(HERE, "amnesia_crec_benchmark_coded.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    print(len(rows), "yes:", sum(r["uses_own_history"] == "yes" for r in rows))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "code":
        code()
    else:
        fetch(sys.argv[2] if len(sys.argv) > 2 else "crec_asym_cache")
