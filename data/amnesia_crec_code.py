"""Hand-coding of the tightened CREC pass (see amnesia_crec_tight.py). Stratum A = all hit granules where a
challenger is named in the same speaker turn as a memory anchor; stratum R = random 50 (seed 2026) of the rest.
Every passage in both strata was read; YES lists the (granule, speaker) codes with uses_own_history=yes, all
other sampled granules are coded no/other with the anchor sentence as quote. Writes amnesia_crec_coded.csv."""
import json,re,csv,collections
P=json.load(open("/home/user/AMNESIA/data/amnesia_crec_tight_passages.json"))
S=json.load(open("/home/user/AMNESIA/data/amnesia_crec_tight_sample.json")); A=set(S["A"]); R=set(S["R"])
g=collections.defaultdict(list)
for p in P: g[p["granuleId"]].append(p)
J="justify_protection_now"; X="argue_against_protection"; O="other"; U="excuse_or_understand_challenger"
H="Mr. HOLLINGS"
# (granule, speaker, purpose, challenger_in_same_speech, quote, note)
YES=[
("CREC-1994-03-07-pt1-PgS28",H,J,"yes","For 200 years, ever since Treasury Secretary Alexander Hamilton wrote his famous ``Report on Manufactures,'' bipartisan majorities of Congress have passed bills to promote industry.","industrial policy; Brits told Hamilton to trade what you produce best"),
("CREC-1994-05-12-pt1-PgS25","Mr. DOLE",J,"yes","Henry Clay, in a speech to Congress in 1824, urged protection of American industries: ``the unprotected manufacturers of a country are exposed to the danger of being crushed in their infancy...''","inserted speech by Under Secretary Garten on the history of antidumping law (Hamilton, Tariff Act of 1816, Clay); used to defend antidumping law; Japan and China discussed"),
("CREC-1994-09-16-pt1-PgE2","Mr. GINGRICH",X,"yes","After all, protective tariffs were also supposed to be a temporary measure until the free enterprise system could get on its feet. Alexander Hamilton would be shocked that we still have them.","analogy used against self-perpetuating boards; past protection as cautionary tale"),
("CREC-1994-11-30-pt1-PgS15",H,J,"yes","The Japanese and all the countries in the Pacific rim follow the federalist Alexander Hamilton of closed markets.","challenger framed as following America's own Hamiltonian model"),
("CREC-1994-12-01-pt1-PgS4",H,J,"yes","But the competition, according to Alexander Hamilton or Friedrich List, is measured not by a cheap shirt or what you can buy but what you can produce.","same granule: Moynihan invokes Hamilton's Report on Manufactures FOR trade (GATT) - see next row"),
("CREC-1994-12-01-pt1-PgS4","Mr. MOYNIHAN",X,"no","If I may just one last time invoke that great West Indian, New Yorker, Alexander Hamilton, and his report on manufacturers, who talked about those misguided nations which sacrificed the interests of a mutually beneficial intercourse to the vain project of selling everything and buying nothing.","Hamilton recruited for the Uruguay Round / free trade"),
("CREC-1995-02-21-pt1-PgE390-2","Mr. HUNTER",O,"yes","Like Alexander Hamilton, he preferred a tariff because, Lincoln suggested, customs collectors on the coast would do less harm to the people than tax collectors roaming their neighborhoods.","Lincoln tribute; tariff as revenue preferred to direct taxes"),
("CREC-1995-05-02-pt1-PgS5961",H,J,"yes","They use the Friedrich List or German model, which Alexander Hamilton initiated in the founding days of this Republic whereby the wealth of a nation is measured not by what it can buy but by what it can produce.","Japan said to use the model Hamilton initiated"),
("CREC-1995-11-09-pt1-PgS16892",H,J,"yes","This ``hands off'' notion of economic development flies in the face of our own history. From Alexander Hamilton's Report on Manufactures, to Henry Clay's ``American System'' of manufacturing, to Lincoln's development of the American rail system... the government has played a crucial role","industrial policy"),
("CREC-1996-09-10-pt1-PgS10155-2",H,J,"yes","And you know what Alexander Hamilton said? He wrote it in a little booklet, ``Reports on Manufacturers.''","standard Hollings Hamilton/Ricardo story"),
("CREC-1996-09-11-pt1-PgS10245-5",H,J,"yes","The Dorgan-Hollings amendment is a wakeup call here to the reality of the greatness of this Nation. Historically, we had this in the very earliest days.","standard Hollings Hamilton/Ricardo story"),
("CREC-1997-03-05-pt1-PgS1945",H,J,"yes","Alexander Hamilton wrote a book that there is one copy of under lock and key over here at the Library of Congress.","also: Lincoln refused English steel for the transcontinental railroad"),
("CREC-1997-11-04-pt1-PgS11632-3",H,J,"yes","Well, Alexander Hamilton wrote ``Report on Manufactures,'' and there is one copy left that I know of over at the Library of Congress under lock and key.","fast-track debate; see also Roth and Reed rows"),
("CREC-1997-11-04-pt1-PgS11632-3","Mr. ROTH",X,"yes","It relates those times when we have forsaken our traditional policy of open commerce in favor of protectionism, as some would have us do now. The Smoot-Hawley tariff and the retaliation it engendered among our trading partners gravely deepened the Great Depression.","own past protection recalled as a cost (Smoot-Hawley), for fast track"),
("CREC-1997-11-04-pt1-PgS11632-3","Mr. REED",O,"no","Beginning with Alexander Hamilton's ``Report On Manufacturers,'' there has been a constant ebb and flow between those that would advise protective tariffs and those that would suggest free, open trade is the only route.","historical framing of the trade debate"),
("CREC-1999-10-26-pt1-PgS13109-7",H,J,"yes","Starting with Alexander Hamilton, in the earliest days of David Ricardo and comparative advantage, and just after the fledgling colonies had won their independence, that the Brits corresponded with Alexander Hamilton...","textiles, Africa/CBI trade bill"),
("CREC-1999-10-27-pt1-PgS13222",H,J,"yes","Do we maintain a strong manufacturing sector and strengthen that economic leg to our national security? Go right back to Alexander Hamilton in the earliest days.",""),
("CREC-1999-10-28-pt1-PgS13378",H,J,"yes","Everybody knows Korea have used the Japanese system of controlled capitalism, and it works. That was the American system under Alexander Hamilton.","challenger framed as using America's own Hamiltonian system"),
("CREC-2000-01-24-pt1-PgS8",H,J,"yes","Alexander Hamilton, in his famous booklet ``Reports on Manufacturers,'' told the Brits to ``bug off.''","also cites the 1789 tariff"),
("CREC-2000-05-10-pt1-PgS3795-3",H,J,"yes","Was Morita making some original observation? Not at all. Alexander Hamilton made the same observation to the British in the early days of 1789.","Akio Morita (Sony) quoted; Japan's view equated with Hamilton's"),
("CREC-2000-09-06-pt1-PgS8048",H,J,"yes","Alexander Hamilton had the wisdom, outlined in the Report on Manufactures.","China PNTR debate"),
("CREC-2000-09-19-pt1-PgS8667-7",H,J,"yes","Alexander Hamilton enunciated the competitive trade policy of the People's Republic of China in 1789.","China PNTR; China framed as following Hamilton; cites 1789 50-percent tariff"),
("CREC-2001-09-10-pt1-PgS9209-3",H,J,"yes","However, the trade debate really was between Thomas Jefferson, the agriculturalist, and Alexander Hamilton, the industrialist.","also Lincoln steel story"),
("CREC-2001-10-04-pt1-PgS10261","Mr. HELMS",J,"yes","Our founding fathers, specifically Alexander Hamilton, understood the importance of manufacturing. The second act of the First Congress imposed tariffs on manufactured goods from abroad.","textiles/manufacturing jobs"),
("CREC-2002-04-29-pt1-PgS3485",H,J,"yes","Hamilton is one of the most disregarded former Treasury Secretaries with a magnificent history of having built this industrial giant, the United States of America.",""),
("CREC-2002-05-23-pt1-PgS4744-2",H,J,"yes","...in our earliest days we had just won our freedom when the David Ricardo comparative advantage crowd in the mother country, Britain, corresponded with Alexander Hamilton","trade promotion authority debate"),
("CREC-2003-07-31-pt1-PgS10469-2",H,J,"yes","We are missing the point of history when everyone talks of this free trade nonsense. I remind them of Alexander Hamilton, a good Republican.","China investment"),
("CREC-2004-02-11-pt1-PgS964-2",H,J,"yes","Alexander Hamilton wrote a little booklet, ``Report On Manufacturers.''",""),
("CREC-2004-03-25-pt1-PgS3182",H,J,"yes","And it's the United States that started it! ... Alexander Hamilton, in his famous ``Report on Manufactures,'' told the Brits, in so many words, to bug off.","op-ed: 1789 50% tariff, Lincoln steel, FDR"),
("CREC-2004-03-25-pt1-PgS3185",H,J,"yes","And it's the United States that started it! ... Alexander Hamilton, in his famous ``Report on Manufactures,'' told the Brits, in so many words, to bug off.","duplicate of the same op-ed"),
("CREC-2004-03-31-pt1-PgS3452","Mr. INOUYE",J,"yes","The second bill ever adopted by Congress, on July 4, 1789, was a 50 percent tariff on numerous articles. This policy of protectionism, endorsed by James Madison and Thomas Jefferson, continued under President Lincoln","'Jobs, Protectionism, and Free Trade': same text as Hollings op-ed, inserted under Inouye; Japan, Korea, China named"),
("CREC-2004-05-11-pt1-PgS5191-2",H,J,"yes","I can point out survival in the very beginning of this Nation started with Alexander Hamilton.","England prevented manufacture in the Colonies"),
("CREC-2004-07-15-pt1-PgS8178",H,J,"yes","Did you know that the United States of America invented globalization? We invented it under Alexander Hamilton.",""),
("CREC-2010-07-28-pt1-PgH6169-4","Mr. LIPINSKI",J,"yes","Our first Secretary of Treasury, Alexander Hamilton, understood the need for a national manufacturing strategy.","National Manufacturing Strategy Act; also Manzullo: 'Alexander Hamilton himself constructed America's first industrial policy in 1791'"),
("CREC-2013-12-03-pt1-PgH7430","Mr. GARAMENDI",J,"yes","Alexander Hamilton came back; we need to build ports, roads, canals. We need to protect American industry with wise laws and trade laws.","Make It In America; Buy American"),
("CREC-2025-04-02-pt1-PgS2121-3","Mr. PAUL",X,"yes","Alexander Hamilton's ``Report on Manufacturers'' is well known. According to Professor Douglas Irwin of Dartmouth College, every tariff recommendation put forth in the report was adopted by Congress in 1792.","resolution against emergency tariffs; history used to argue tariff power belongs to Congress ('no taxation without representation')"),
]
NO_NOTES={"CREC-2015-01-27-pt1-PgH622-2":"Hamilton cited for infrastructure only (Chinese steel complaint elsewhere); not protection",
"CREC-2015-07-14-pt1-PgH5159-5":"Hamilton cited for infrastructure only; not protection",
"CREC-2022-07-26-pt1-PgS3670-2":"'take a page out of our own history' = federal R&D, not protection/imitation",
"CREC-1998-06-19-pt1-PgE1175-2":"infant industries refers to Japan's own past protection, not the US",
"CREC-2000-05-24-pt1-PgH3662-2":"infant industries quoted from a Chinese official; Clay as orator",
"CREC-1997-06-24-pt1-PgH4257":"'old infant industries argumentation' of other nations, no US history",
"CREC-1998-07-22-pt1-PgH6111":"'old infant industries argumentation' of other nations, no US history",
"CREC-2005-04-20-pt1-PgH2192-2":"infant industries = renewables today",
"CREC-2006-06-28-pt1-PgS6615-4":"Hamilton's import duties as revenue/Treasury history",
"CREC-1998-10-12-pt1-PgS12383-2":"Coast Guard history (cutters to enforce tariffs)",
"CREC-1994-08-09-pt1-PgS44":"Coast Guard history (cutters to enforce tariffs)",
"CREC-2014-05-14-pt1-PgS2994-4":"infant industry = wind PTC today",
"CREC-2018-03-08-pt1-PgS1529-7":"Clay cited for infrastructure",
"CREC-2004-02-09-pt1-PgS695-2":"Clay cited for highways/infrastructure",}
yesg={y[0] for y in YES}
for y in YES: assert y[0] in g, y[0]
for k in NO_NOTES: assert k in g, k
def url(gid): return f"https://www.govinfo.gov/app/details/{g[gid][0]['packageId']}/{gid}"
def sent(p):
    w=p["window"]; a=p["anchor"]; j=w.lower().find(a.lower())
    s=w.rfind(". ",0,j); s=0 if s<0 else s+2; e=w.find(". ",j); e=len(w) if e<0 else e+1
    return w[s:e][:400].strip()
rows=[]
for gid in sorted(A|R):
    ps=g[gid]; st="challenger_same_passage_all" if gid in A else "random50_of_rest"
    base=dict(granule_id=gid,year=int(ps[0]["date"][:4]),chamber=ps[0]["chamber"],title=ps[0]["title"][:120],stratum=st,url=url(gid))
    if gid in yesg:
        for y in YES:
            if y[0]==gid:
                rows.append(base|dict(speaker=y[1],uses_own_history="yes",purpose=y[2],challenger_in_same_speech=y[3],quote=y[4],note=y[5]))
        continue
    cand=[p for p in ps if (p["challenger_in_turn"] or gid in R)]
    cand.sort(key=lambda p:(p["anchor"].lower()=="when we were", not p["trade_in_window"]))
    p=cand[0]
    rows.append(base|dict(speaker=p["speaker"],uses_own_history="no",purpose="other",challenger_in_same_speech="yes" if gid in A else "no",
        quote=sent(p),note=NO_NOTES.get(gid,f"anchor '{p['anchor']}' used in unrelated sense")))
cols=["granule_id","year","chamber","speaker","uses_own_history","purpose","challenger_in_same_speech","stratum","quote","note","title","url"]
with open("/home/user/AMNESIA/data/amnesia_crec_coded.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols); w.writeheader(); w.writerows(rows)
import pandas as pd
d=pd.DataFrame(rows); print(len(d), d.granule_id.nunique())
print(d.groupby(["stratum","uses_own_history"]).granule_id.nunique())
y=d[d.uses_own_history=="yes"]; print(y.groupby(["purpose","challenger_in_same_speech"]).size())
y["dec"]=y.year//10*10; print(y.groupby(["dec","purpose"]).size().unstack(fill_value=0))
print(y.speaker.value_counts())
P2=pd.DataFrame(P); P2["year"]=P2.date.str[:4].astype(int)
gg=P2.drop_duplicates("granuleId"); print("hits by decade", (gg.year//10*10).value_counts().sort_index().to_dict())
A_=gg[gg.granuleId.isin(A)]; print("A by decade",(A_.year//10*10).value_counts().sort_index().to_dict())
