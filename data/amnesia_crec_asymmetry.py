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

Reproduction check: for A over 1994-2025 the API reports count = 6,013 (as in the earlier run), but
paging returns 6,011 distinct granule ids: in 2025 two granules are listed twice
(CREC-2025-03-11-pt1-PgS1662-6, CREC-2025-03-11-pt1-PgH1133). The csv gives distinct granules (6,011).
A AND MEM reproduces 748 distinct granules, and all 33 granules coded uses_own_history=yes in
amnesia_crec_coded.csv are among them.

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
CODES = {
    'CREC-1994-02-22-pt1-PgS14': ('Ms. MOSELEY-BRAUN', "no", "other", 'no',
        'As a testament for his administration, it was written in concert with James Madison and Alexander Hamilton.',
        'balanced budget amendment; Hamilton on public credit/debt, not protection'),
    'CREC-1994-02-25-pt1-PgH11': ('Mr. PACKWOOD', "no", "other", 'yes',
        'In the First Congress, Alexander Hamilton, who was the first Secretary of the Treasury, tried to come forth with an Executive budget, and Congress rejected it.',
        "balanced budget; Hamilton's executive budget, Clay on executive power; not protection"),
    'CREC-1995-03-20-pt1-PgS4165': ('Mr. ASHCROFT', "no", "other", 'no',
        'They have asked for it even in times when we were not facing the overwhelming deficits we are facing now.',
        "line-item veto; anchor 'when we were' used in unrelated sense"),
    'CREC-1995-05-01-pt1-PgS5874': ('Mr. COHEN', "no", "other", 'no',
        'No less of a proponent of a strong national government than Alexander Hamilton fully understood the genius of a system that divided powers between the national and State governments.',
        'product liability; Hamilton on federalism (Federalist 17)'),
    'CREC-1995-06-07-pt1-PgS7803': ('Mr. SIMON', "no", "other", 'yes',
        'I can remember when we were debating this issue when I was in the Illinois General Assembly and a man was about to be executed, and suddenly someone in the State of Georgia confessed that he had committed the crime.',
        "terrorism/death penalty; anchor 'when we were' used in unrelated sense"),
    'CREC-1995-07-17-pt1-PgS10086-3': ('Mr. CHAFEE', "no", "other", 'no',
        'In 1982, Senator Bumpers had an amendment that came out of the committee when we were doing regulatory reform in that year, which had exactly the same language that we--I and others on this side--are objecting to, and that Senator Hatch and others put into this bill.',
        "regulatory reform; anchor 'when we were' used in unrelated sense"),
    'CREC-1995-07-18-pt1-PgS10189-4': ('Mr. LEVIN', "no", "other", 'no',
        'And that is why, when we were considering the Nunn-Coverdell amendment, I noticed that I thought this was going to hurt small businesses and small governments because they are going to lose the opportunity of learning about the impact of a rule from rulemaking so that they can challenge those critical issues after the final rule is adopted.',
        "regulatory reform; anchor 'when we were' used in unrelated sense"),
    'CREC-1995-11-17-pt2-PgS17247': ('Mr. SIMPSON', "no", "other", 'no',
        'I know all veterans will join now--as we all did when we were called to arms--in defense of the Nation, and to assure peace, prosperity, and stability for our children and grandchildren.',
        "budget reconciliation omnibus; veterans 'when we were called to arms'"),
    'CREC-1996-06-24-pt1-PgS6680': ('Mr. BENNETT', "no", "other", 'no',
        'At that time, there were many people who were afraid of the impact the Constitution would have on their existing Government, and to allay those fears, James Madison, along with John Jay and Alexander Hamilton, set forth the clear statement of the intellectual and philosophical underpinnings of American Government.',
        'campaign finance; Hamilton as Federalist author'),
    'CREC-1997-02-12-pt1-PgS1300-2': ('Mr. ASHCROFT', "no", "other", 'no',
        "Because, as Alexander Hamilton aptly noted more than two centuries ago, ``Here, Sir, the people govern.'' These assertions also stand at odds with the great triumph of individualism that is America.",
        'term limits; Hamilton quoted on popular government'),
    'CREC-1997-10-01-pt1-PgS10245-5': ('Mr. CAMPBELL', "no", "other", 'no',
        "I point out a couple of things: It has been 5 years in which most of the Members voted down a cost-of-living increase for themselves; also, as they both remember when we were here on the floor with this bill a month or so ago, it was Senator Brownback's [[Page S10248]] amendment and cosponsored by Senator Wellstone and me to delete that COLA increase from the original bill.",
        "appropriations/COLA; anchor 'when we were' used in unrelated sense"),
    'CREC-1998-06-04-pt1-PgH4078-4': ('Mr. WATT of North Carolina', "no", "other", 'no',
        'We can have Alexander Hamilton or we can have Istook.',
        'religious freedom amendment; Hamilton as Founder'),
    'CREC-2001-03-15-pt1-PgS2324-2': ('Mr. WELLSTONE', "no", "other", 'yes',
        'basically last week when we were dealing with repetitive stress injury, we took a rule that was a result of 10 years of work',
        "bankruptcy reform; anchor 'when we were' used in unrelated sense"),
    'CREC-2001-12-20-pt1-PgS13871': ('Mr. BREAUX', "no", "other", 'no',
        'That was a poor model for national security when we were fighting drugs and international smuggling--and it is totally inadequate after September 11 as we face the threat of terrorism.',
        "port security; anchor 'when we were' used in unrelated sense"),
    'CREC-2004-02-02-pt1-PgS343': ('The PRESIDING OFFICER', "no", "other", 'no',
        'I was also involved on this committee in 1998 when we were putting together TEA-21.',
        "highway bill; anchor 'when we were' used in unrelated sense"),
    'CREC-2004-03-11-pt1-PgH1063': ('Mr. BURGESS', "no", "other", 'no',
        "Because after all, the consumer is going to be more wise with spending their money than they are with someone else's money, and I think someone made the point on the floor of this House back when we were having this debate about, you never spend money washing a rented car.",
        "health savings accounts; anchor 'when we were' used in unrelated sense"),
    'CREC-2005-04-11-pt1-PgS3403': ('Mrs. MURRAY', "no", "other", 'yes',
        'Infant industries must grow up.',
        "Airbus launch aid; 'infant industries must grow up' quoted from a commentary about European subsidies, no US history"),
    'CREC-2005-11-16-pt1-PgS12884-2': ('Mr. KENNEDY', "no", "other", 'no',
        'I think when we were getting started, in terms of the debate on pension reform, most Americans were wondering what the Congress was going to do about these issues.',
        "pension reform; anchor 'when we were' used in unrelated sense"),
    'CREC-2007-03-09-pt1-PgH2351-2': ('Mr. OBERSTAR', "no", "other", 'no',
        'There was a time when we were investing $6 billion a year in Federal funds, matched by State and local dollars, to build sewage treatment facilities, raise them to tertiary treatment, removing nutrients, adding oxygen, returning clean water to the receiving waters.',
        'water quality; past federal sewage investment, not protection'),
    'CREC-2007-09-11-pt1-PgS11356-3': ('Mr. CORNYN', "no", "other", 'yes',
        'Today, 6 years to the day from when we were first attacked, we must redouble our efforts.',
        "appropriations/Iraq; 'when we were first attacked' (9/11)"),
    'CREC-2008-05-14-pt1-PgH3784': ('Mr. HASTINGS of Washington', "no", "other", 'no',
        'Last night when we were up in the Rules Committee---- Mr.',
        "farm bill rule; anchor 'when we were' used in unrelated sense"),
    'CREC-2008-09-26-pt1-PgS9723': ('(bill text)', "no", "other", 'yes',
        "(a) Study.-- (1) In general.--The Secretary of the Interior (referred to in this section as the ``Secretary''), in consultation with the Governor of the Virgin Islands, shall conduct a special resource study of Estate Grange and other sites and resources associated with Alexander Hamilton's life on St.",
        'amendment text; study of Hamilton sites on St. Croix'),
    'CREC-2010-05-12-pt1-PgS3569-9': ('Mr. WARNER', "no", "other", 'no',
        'I think those of us on the committee when we were drafting the legislation wanted to make sure that the mortgage security securitization process, the originators of mortgages, had skin in the game.',
        "financial reform; anchor 'when we were' used in unrelated sense"),
    'CREC-2011-07-13-pt1-PgS4542': ('Mr. BENNET', "no", "other", 'no',
        'But it is almost as though Alexander Hamilton, who wrote these words in 1787, were sitting here today.',
        'debt ceiling; Hamilton (Federalist 30) on public credit'),
    'CREC-2013-08-01-pt1-PgH5276-3': ('Mr. COLE', "no", "other", 'no',
        "In the last couple of years, we have actually passed seven pieces of legislation when we were in the majority--they obviously had to go through a Democratic Senate and to the President's desk--that changed or modified ObamaCare--and saved, by the way, about $62 billion.",
        "REINS Act rule; anchor 'when we were' used in unrelated sense"),
    'CREC-2013-09-11-pt1-PgS6350-4': ('Mr. WHITEHOUSE', "no", "other", 'no',
        'We discussed it at length with Senator Collins of Maine when we were trying to add it to the Transportation and HUD appropriations bill, and I believe we have worked through issues presented by her office and issues presented by Senator Coburn.',
        "energy efficiency bill; anchor 'when we were' used in unrelated sense"),
    'CREC-2014-07-28-pt1-PgH6899': ('Ms. JACKSON LEE', "no", "other", 'no',
        'What I would say is that, when we were crafting this bill along with my chairwoman as she introduced this legislation, we were somewhat before this rising surge, and we began to think about what we needed to do to get in front of it.',
        "CBP authorization; anchor 'when we were' used in unrelated sense"),
    'CREC-2019-05-16-pt1-PgH3853-5': ('Mr. WALDEN', "no", "other", 'no',
        "When we were in charge, 45 percent--45 percent--were the minority's amendments that came to the floor.",
        "health outreach bill; anchor 'when we were' used in unrelated sense"),
    'CREC-2019-05-23-pt1-PgH4153': ('Mr. GOHMERT', "no", "other", 'yes',
        "He was defeated by Andrew Jackson and defeated fairly easily because people thought he had cheated to win by making a deal he didn't make with Henry Clay.",
        "Gohmert on J.Q. Adams and Clay's 'corrupt bargain'; passing mention of a tariff under Adams, no argument about protection"),
    'CREC-2025-02-11-pt1-PgH623': ('Ms. STEVENS', "no", "other", 'no',
        'Nowhere in that process, when we were working with the troubled asset relief program dollars, did anyone dare to think about going into the Bureau of Fiscal Service and tapping the wires and the accounts of the American public and jolting and shaking the very foundation of trust.',
        "midnight rules bill; anchor 'when we were' used in unrelated sense"),
}


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
