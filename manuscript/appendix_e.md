# Appendix E: Salience of incumbent responses during the absorption phase

*Draft, 21 November 2026. Inter-coder reliability pending (second coding in progress). Not for submission.*

## E.1 Purpose

The primary claim holds that binding incumbent escalation follows measurable sectoral displacement. The claim would be circular if responses before displacement were simply not recorded or not coded. This appendix therefore codes every documented incumbent response in the absorption phase with the same rubric used for the post-displacement phase. For the German case it also adds an independent measure of attention from parliamentary debate. If absorption-phase responses were as frequent and as severe as post-displacement responses, the sequencing claim would fail.

## E.2 Definitions

**Displacement milestone.** For each contested sector we date the first year in which the challenger reaches world leadership or a measurable lead over the incumbent in that sector: production, export or market-share leadership (Table E1). A case has several sectoral milestones; responses aimed at the challenger's economy as a whole are dated against the case's first milestone.

**Absorption phase.** The years before a sector's displacement milestone. A response falls in the absorption phase if it precedes the milestone of its sector; the lag is the response year minus the milestone year.

**Manifest Salience Score (MSS).** Each response is scored on an ordinal scale from 1 to 5. The score measures how binding the instrument is, not how loud the debate around it is:

| MSS | Level | Rule |
|---|---|---|
| 1 | Rhetoric | public statement without an official procedure |
| 2 | Procedure | official investigation, hearing, petition or WTO complaint; nothing binding yet |
| 3 | Narrow binding | binding but narrow: origin marking, patent rule, duty on a single product |
| 4 | Sectoral binding | binding quantity or price limit for a whole sector, or trade statute creating new sanction powers |
| 5 | Broad binding or denial | tariffs on a large share of imports, or denial of technology to a sector or a national champion |

In borderline cases the lower score applies. Measures that only strengthen the incumbent's own economy (education acts, the CHIPS and Science Act) are excluded.

## E.3 Data

DS1 contains 17 sectoral milestones and 41 incumbent responses across the four cases (files `ds1_milestones.csv`, `ds1_responses.csv`, `ds1_events.csv`). Each row cites its source. For Japan, three sectors with disputes before 1980 were added to avoid an artificially empty absorption phase: cotton textiles (milestone 1951), colour television (1970) and steel (1969). For Germany, beet sugar (milestone 1880) was added after the parliamentary record showed it to be the first sector in which Germany became a political issue (Section E.6).

**Table E1. Sectoral displacement milestones**

| Case | Sector | Year | Milestone | Source |
|---|---|---|---|---|
| China | manufacturing overall | 2010 | China overtakes US in manufacturing value added (19.8 vs 19.4 percent) | IHS Global Insight via AEI (2011) |
| China | solar PV | 2012 | China dominant in solar manufacturing (dating ranges 2008 to 2012 across files) | IEA (2022) |
| China | telecom equipment | 2012 | Huawei overtakes Ericsson in total revenue (equipment-only measure: 2017) | China.org.cn (2012); Caixin (2018) |
| China | electric vehicles | 2023 | BYD overtakes Tesla in quarterly BEV sales (Q4 2023: 526409 vs 484507) | InsideEVs (2024) |
| China | advanced logic chips | 2023 | TechInsights confirms SMIC 7nm in Huawei Mate 60 Pro (September 2023) | TechInsights (2023) |
| Germany | synthetic dyes | 1870 | Germany holds about half of world dye output (primary German milestone; corroborated by Royal Commission 1885-86 per handover) | Murmann and Homburg (2001) |
| Germany | beet sugar | 1880 | Continental (chiefly German) beet sugar overtakes cane in the British market in the 1880s; Germany about one third of British unrefined sugar imports by 1890 | Oxford Companion to Sugar and Sweets; Estudos Economicos (SciELO) on European sugar policy and Brazilian exports; Hansard HL 26 May 1884 |
| Germany | steel | 1893 | German steel output exceeds British | Encyclopaedia Britannica: Germany - The economy 1890-1914 |
| Germany | electrical engineering | 1900 | AEG and Siemens among world leaders; Germany about half of world electrical exports by 1913 | Kocka (1999); Reindl (1997) |
| Japan | cotton textiles | 1951 | Japan again the world's largest exporter of cotton textiles | USDA FAS ATO Tokyo (2010) The History of U.S. Cotton in Japan; Osaka University Discussion Paper 99-06 |
| Japan | steel | 1969 | Japan becomes the world's largest steel exporter | Ohashi (2005) Journal of International Economics: Learning by doing export subsidies and industry growth (Japanese steel 1950s-60s) |
| Japan | colour television | 1970 | Japanese share of US market for middle-sized colour receivers about 30 percent (Japan led world colour TV production from the late 1960s) | US Tariff Commission (1971) TC Publication 367; UQ RSMG Working Paper 26 |
| Japan | automobiles | 1980 | Japan overtakes US as largest car producer (about 7.0m vs 6.4m) | Sobel (1984); Toyota 75-year history |
| Japan | DRAM | 1981 | Japanese 64K generation overtakes US producers | Semiconductor History Museum of Japan |
| Japan | semiconductors overall | 1987 | Japan overtakes US in overall semiconductor share (48 vs 39 percent) | Okada (2005); AMRO (2025) |
| Korea | DRAM | 1992 | Samsung becomes largest DRAM maker (about 13.5 vs 12.8 percent for Toshiba) | Harvard Business School (2003); Samsung Semiconductor |
| Korea | shipbuilding | 2000 | Korea overtakes Japan in shipbuilding market share | ORF (2025); GlobalSecurity.org |

## E.4 Results

**Table E2. Incumbent responses by case and phase**

| Case | Phase | Responses | Binding | MSS ≥ 4 | Max MSS |
|---|---|---|---|---|---|
| Germany | absorption | 0 | 0 | 0 | – |
| Germany | post | 6 | 3 | 1 | 5 |
| Japan | absorption | 1 | 0 | 0 | 2 |
| Japan | post | 14 | 11 | 8 | 4 |
| Korea | absorption | 2 | 1 | 0 | 3 |
| Korea | post | 5 | 2 | 0 | 3 |
| China | absorption | 2 | 1 | 1 | 5 |
| China | post | 9 | 6 | 4 | 5 |
| **All** | **absorption** | **5** | **2** | **1** | **5** |
| **All** | **post** | **34** | **22** | **13** | **5** |

Five of 39 responses precede the milestone of their sector. Four of the five score 3 or lower: a dumping complaint on Japanese television receivers (1968, MSS 2), the Section 301 investigation of Korea's intellectual-property regime (1985, MSS 2) and the resulting US–Korea agreement (1986, MSS 3), and a speech by the US National Security Adviser (2022, MSS 1).

**The bounded exception.** The US export controls on advanced computing and semiconductor manufacturing of 7 October 2022 score MSS 5 and precede the confirmation of SMIC's 7 nm production in September 2023 by one year. They are the only binding instrument in the dataset designed to prevent rather than answer displacement. We report them as the limiting case of the pattern rather than redefine the milestone: one instrument in one sector, embedded in a campaign of tariffs and entity listings that followed China's manufacturing and telecommunications milestones by one to eight years.

## E.5 Parliamentary attention, Britain and Germany 1850–1914

As an independent check we count mentions of Germany (including Prussia and the Zollverein) in all economic debates of the House of Commons and the House of Lords recorded in Historic Hansard, 1850–1914. Economic debates are selected by a fixed title filter (version `econ_v2`; 15,126 of 281,577 debates). A second indicator flags debates in which Germany appears within 30 words of a competition term (competition, dumping, unfair, bounty, subsidy, undersell, cheap, imitation, rival).

**Table E3. Germany in British economic debates, pooled by period**

| Period | Economic debates | Mentioning Germany | Germany near a competition term | Mentions per 100,000 words |
|---|---|---|---|---|
| 1850–1869 (absorption) | 1,054 | 4.7 % [3.6–6.2] | 0.9 % [0.5–1.6] | 14.4 |
| 1870–1892 | 3,523 | 3.3 % [2.8–3.9] | 0.6 % [0.4–0.9] | 20.1 |
| 1893–1902 | 3,430 | 6.2 % [5.5–7.1] | 1.0 % [0.7–1.4] | 44.5 |
| 1903–1914 | 6,376 | 8.8 % [8.1–9.5] | 1.4 % [1.1–1.7] | 42.6 |

Brackets: 95 % Wilson intervals.

Figure E1 (`figures/fig_e1_hansard.pdf`) shows the annual series. Parliamentary attention to Germany roughly triples after the steel milestone of 1893 and stays high through the Tariff Reform campaign. Before 1870, Germany appears in economic debates mostly as a trading partner or transit route, for example in the debates on trade with Russia during the Crimean War, not as a competitor.

Two qualifications follow. First, attention does not rise after the dye milestone of 1870 itself; it rises after steel. Second, the competition indicator differs little between the absorption phase and the 1870s and 1880s, and the early annual values rest on very few debates. The parliamentary record therefore supports the ordering (attention follows displacement) but dates the escalation to the second, broader milestone.

## E.6 Sector-level check

Aggregate attention mixes sectors with very different political weight. We therefore split the economic debates by sector: a debate belongs to a sector if it uses at least three sector terms, and it links Germany to that sector if Germany appears within 30 words of a sector term. The number of debates on a sector over the whole period serves as a first measure of its political weight; census employment will replace it as a robustness check once the census tables are obtained.

**Table E4. Germany in British sector debates before and after the sector milestone**

| Sector | Milestone | Debates on the sector, 1850–1914 | Germany linked, before | Germany linked, after |
|---|---|---|---|---|
| Beet sugar | 1880 | 574 | 2.7 % of 75 [0.7–9.2] | 17.2 % of 499 [14.2–20.8] |
| Iron and steel | 1893 | 172 | 14.6 % of 48 [7.2–27.2] | 24.2 % of 124 [17.5–32.4] |
| Dyes and chemicals | 1870 | 18 | 0 of 1 | 29.4 % of 17 [13.3–53.1] |

Brackets: 95 % Wilson intervals.

The clearest break occurs in sugar, the sector with the most political voice: Germany is almost absent from British sugar debates before the rise of bounty-fed beet sugar and appears in about one sugar debate in six afterwards, ending in the Brussels Sugar Convention of 1902. Steel shows the same direction with overlapping intervals. Dyes, where German displacement came first, were almost never debated at all. This refines the primary claim: escalation follows displacement in sectors that have political voice in the incumbent. The long lag between the dye milestone and the Patents and Designs Act of 1907 is consistent with this reading.

## E.7 Comparison: the United States

The United States overtook Britain in GDP per capita around 1900 (Maddison Project 2023). If displacement alone triggered escalation, British attention to the United States should rise as well. It does not. Mentions of the United States per 100,000 words of economic debate stay between 41 and 56 across all four periods (Germany: 14 rising to 43–45), and the share of debates linking the United States to competition terms stays near one per cent. We read this as a scope condition rather than a refutation: American growth before 1914 displaced Britain mainly in the American home market and in output, not in Britain's contested export markets, which is where the primary claim locates the trigger. This reading is not yet tested and is flagged as such.

## E.8 Limitations

1. **Second coder.** All MSS scores currently come from one coder. Inter-coder agreement (Krippendorff's α, ordinal) will be reported here.
2. **Parliamentary check only for Britain.** Machine-readable full text of the US Congressional Record before 1994 is not openly available; the Japanese and Korean cases rest on the coded instruments alone.
3. **Milestone sources.** The Japanese steel milestone (1969, largest exporter) rests on a single secondary source; the voluntary restraint arrangement took effect in the same year (lag 0). Several Chinese milestones depend on the chosen measure (telecom equipment: revenue 2012 or equipment sales 2017).
4. **Title filter.** Economic debates are identified by title. Debates on economic matters under other titles, for example within question time, are missed.
