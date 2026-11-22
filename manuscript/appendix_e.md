# Appendix E: Salience of incumbent responses during the absorption phase

*Draft, 21 November 2026. Inter-coder reliability pending (second coding in progress). Not for submission.*

## E.1 Purpose

The primary claim holds that binding incumbent escalation follows measurable sectoral displacement. The claim would be circular if responses before displacement were simply not recorded or not coded. This appendix therefore codes every documented incumbent response in the absorption phase with the same rubric used for the post-displacement phase. For the German case it also adds an independent measure of attention from parliamentary debate. If absorption-phase responses were as frequent and as severe as post-displacement responses, the sequencing claim would fail.

## E.2 Definitions

**Displacement milestone.** For each contested sector we date the first year in which the challenger leads in the market where the incumbent sells: export markets for Britain, the world market or the American home market for the United States, the world market for Japan and the European Union (Table E1). A case has several sectoral milestones; responses aimed at the challenger's economy as a whole are dated against the case's first milestone. As a robustness check we apply a uniform export rule: the first year in which the challenger's exports to the world reach those of the incumbent (Table E1b, Section E.4).

**Absorption phase.** The years before a sector's displacement milestone. A response falls in the absorption phase if it precedes the milestone of its sector; the lag is the response year minus the milestone year.

**Instrument Reach score (IR).** Each response is scored on an ordinal scale from 1 to 5. The score measures how binding the instrument is, not how loud the debate around it is:

| IR | Level | Rule |
|---|---|---|
| 1 | Rhetoric | public statement without an official procedure |
| 2 | Procedure | official investigation, hearing, petition or WTO complaint; nothing binding yet |
| 3 | Narrow binding | binding but narrow: origin marking, patent rule, duty on a single product |
| 4 | Sectoral binding | binding quantity or price limit for a whole sector, or trade statute creating new sanction powers |
| 5 | Broad binding or denial | tariffs on a large share of imports, or denial of technology to a sector or a national champion |

In borderline cases the lower score applies. Measures that only strengthen the incumbent's own economy (education acts, the CHIPS and Science Act) are excluded.

## E.3 Data

DS1 contains 18 sectoral milestones (the electric-vehicle milestone is split by incumbent) and 41 incumbent responses across the four cases (files `ds1_milestones.csv`, `ds1_responses.csv`, `ds1_events.csv`). Each row cites its source. For Japan, three sectors with disputes before 1980 were added to avoid an artificially empty absorption phase: cotton textiles (milestone 1951), colour television (1970) and steel (1969). For Germany, beet sugar (milestone 1880) was added after the parliamentary record showed it to be the first sector in which Germany became a political issue (Section E.6).

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

**Table E1b. Contested market and export-rule check**

| Case | Sector | Main milestone | Contested market | Export rule | Basis |
|---|---|---|---|---|---|
| China | manufacturing overall | 2010 | world output | 2005 | Comtrade SITC 5-8 |
| China | solar PV | 2012 | world market | 2006 | Comtrade HS 854140 gegen Deutschland |
| China | telecom equipment | 2012 | world market | 2006 | Comtrade HS 8517 |
| China | electric vehicles | 2023 | world market (BEV sales) | 2021 | Comtrade HS 870380 gegen USA: China 8.6, USA 4.6 Mrd. USD (2021) |
| China | advanced logic chips | 2023 | capability, not market lead | not meaningful | HS 8542: Chinas Ausfuhren schon 2017 hoeher, ueberwiegend Montage fremder Chips |
| China | electric vehicles | 2023 | world market (BEV sales) | not reached by 2024 | Comtrade HS 870380 gegen Deutschland: 32.0 zu 41.1 Mrd. USD (2024) |
| Germany | synthetic dyes | 1870 | world market (output share) | by 1899 | Tyszynski 1951: Chemie DEU/GBR 1.43 im ersten Benchmarkjahr |
| Germany | beet sugar | 1880 | British home market | no series |  |
| Germany | steel | 1893 | world output; export markets near parity only by 1913 | not reached by 1913 | Tyszynski 1951: DEU/GBR 0.35 (1899), 0.91 (1913) |
| Germany | electrical engineering | 1900 | world market | by 1913 | Tyszynski 1951: DEU/GBR 0.58 (1899), 2.11 (1913) |
| Japan | cotton textiles | 1951 | world export market | 1951 | Meilenstein selbst exportbasiert |
| Japan | steel | 1969 | world export market | by 1962 | Comtrade SITC 67, erstes Datenjahr |
| Japan | colour television | 1970 | US home market | 1963 | Comtrade SITC 7241 |
| Japan | automobiles | 1980 | world output and US home market | 1970 | Comtrade SITC 7321 |
| Japan | DRAM | 1981 | world market | 1984 | Comtrade SITC 776 (alle Halbleiter) |
| Japan | semiconductors overall | 1987 | world market | 1984 | Comtrade SITC 776 |
| Korea | DRAM | 1992 | world market | not measurable | SITC 776 trennt DRAM nicht von Logikchips; Korea/USA 0.39 im Jahr 2004 |
| Korea | shipbuilding | 2000 | world market | 2001 | Comtrade HS 89 (SITC-2-Reihe 793 endet 2000 bei 0.80); Korea/Japan 1.15 im Jahr 2001 |

Export-rule data: UN Comtrade (SITC Rev. 1 and 2, HS), exports to the world as reported by the exporter, current US dollars; Germany before 1914: Tyszynski (1951) benchmarks.

## E.4 Results

**Table E2. Incumbent responses by case and phase**

| Case | Phase | Responses | Binding | IR ≥ 4 | Max IR |
|---|---|---|---|---|---|
| Germany | absorption | 0 | 0 | 0 | – |
| Germany | post | 8 | 4 | 2 | 5 |
| Japan | absorption | 1 | 0 | 0 | 2 |
| Japan | post | 14 | 11 | 8 | 4 |
| Korea | absorption | 2 | 1 | 0 | 3 |
| Korea | post | 5 | 2 | 0 | 3 |
| China | absorption | 2 | 1 | 1 | 5 |
| China | post | 9 | 6 | 4 | 5 |
| **All** | **absorption** | **5** | **2** | **1** | **5** |
| **All** | **post** | **36** | **23** | **14** | **5** |

Five of 41 responses precede the milestone of their sector. Four of the five score 3 or lower: a dumping complaint on Japanese television receivers (1968, IR 2), the Section 301 investigation of Korea's intellectual-property regime (1985, IR 2) and the resulting US–Korea agreement (1986, IR 3), and a speech by the US National Security Adviser (2022, IR 1).

**The bounded exception.** The US export controls on advanced computing and semiconductor manufacturing of 7 October 2022 score IR 5 and precede the confirmation of SMIC's 7 nm production in September 2023 by one year. They are the only binding instrument in the dataset designed to prevent rather than answer displacement. We report them as the limiting case of the pattern rather than redefine the milestone: one instrument in one sector, embedded in a campaign of tariffs and entity listings that followed China's manufacturing and telecommunications milestones by one to eight years.


**Robustness: the export rule.** Under the uniform export rule 28 of the 41 responses follow the export crossover, 3 cannot be placed because only an upper bound exists for the crossover (British responses of 1885–1896 against an export lead in chemicals documented first in 1899), and 9 cannot be classified because the export data do not measure the contested product: DRAM is not separable from logic chips in SITC 776, and China's integrated-circuit exports consist largely of assembled foreign chips. One response precedes the export crossover: the EU's countervailing duties on Chinese battery-electric vehicles of October 2024 (IR 4), imposed while Chinese electric-car exports were still below German exports (32.0 against 41.1 billion US dollars in 2024). Against the United States, Chinese exports had passed American ones in 2021, three years before the American tariff increase. The two rules thus produce one bounded exception each, in different sectors: export controls on advanced chips under the main rule, EU duties on electric cars under the export rule. Neither rule produces a systematic pattern of binding escalation before displacement.

**Statistical tests.** Within ten years on either side of the milestone, 5 responses fall in the ten years before and 26 in the ten years from the milestone (binomial test against equal probability, one-sided p = 0.0001); for binding responses the counts are 2 and 18 (p = 0.0002). In a placebo exercise that shifts every milestone by a random number of years between −10 and +10 (10,000 draws, all responses of a milestone shifted together), the mean share after the milestone is 0.60; a share as high as the observed 0.84 occurs in 2.2 per cent of draws for all responses and in 0.7 per cent for binding responses (0.90).

**Business cycle.** Temporary trade barriers rise in downturns (Bown and Crowley 2013b). If milestones coincided with recessions, the sequence could reflect the cycle. It does not appear to. Measuring the incumbent's output gap as the deviation of log real GDP from a Hodrick-Prescott trend (λ = 100; Maddison Project 2023), 38 per cent of the 39 responses with data fall in years of negative output gap, against 45 per cent of all years in the case windows; for binding responses the shares are 39 and 45 per cent (`data/tests_cycle.py`).

**Register check.** The 41 responses were collected from the literature on major disputes. As an independent frame, the Temporary Trade Barriers Database (Bown 2016) lists all 759 antidumping and countervailing duty cases of the United States and the European Union against Japan, Korea and China from 1980 to 2015 (`data/registers_ttbd.py`). Against Korea, 67 of 181 cases precede the DRAM milestone (35 with definitive duties); against China, 316 of 414 precede the manufacturing milestone (231 with definitive duties); the Japanese milestones mostly predate the database. These cases are narrow (IR 2 or 3) and follow displacement at product level: for 127 American antidumping cases against China (1996–2015), China's share of American imports of the products concerned rose from a median of 15 to 23 per cent between four years and one year before the case, and rose in 82 per cent of cases (UN Comtrade; `data/registers_product_displacement.py`). The finding refines the claim: the reach of the instrument matches the reach of displacement.

**Complete register and population (referee findings 1 and 2).** `data/broad_register.csv` lists 23 broad American instruments (IR 4–5) against Japan, Korea and China from 1957 to 2024, compiled from the USITC's list of Section 201 safeguard protection 1975–2016 (USITC Centennial History, Table 10.1), bilateral restraint agreements, Sections 232 and 301, and the Export Administration Regulations. For 31 instrument–target pairs, `data/population_test.py` dates the first year in which the challenger's world exports of the products concerned reached US exports (UN Comtrade; SITC Rev. 1 for 1962–1999, Rev. 3 for 1992–2009, HS four-digit for 2008–2023; at least 50 million US dollars and sustained in three of the following four years). Result: 22 pairs after the crossover (10 of them with the crossover in the first data year), 4 before, 5 not datable. The four: Korea under the cotton-textile LTA of 1962 and the textile agreements of 1971 (substantive), Japan under the 1986 semiconductor agreement (artefact of the broad SITC group; DRAM crossed in 1981), China under the global steel safeguard of 2002 (not targeted). Population: of the manufacturing groups in which a challenger's exports overtook US exports, a targeted broad instrument followed within ten years in 22 per cent for Japan (41 groups), 20 per cent for Korea (25 groups in SITC Rev. 1; none of 13 in Rev. 3), 1 per cent for China excluding the 2018 Section 301 tariffs (312 groups) and 74 per cent of China's post-2008 groups including them (`data/population_hazard.csv`). Target countries for several Section 201 actions are taken from secondary literature and marked in the register.

**Control group and weight.** `data/population_panel.py` builds a panel of group × year for every manufacturing group in which the challenger exported at least 50 million US dollars in some year (1,316 group series: Japan 90 and Korea 88 in SITC Rev. 1; Korea 156 and China 163 in Rev. 3; China 819 in HS four-digit), with the state "post" from the crossover year. Poisson models with year effects, standard errors clustered by group (`data/population_panel.txt`):

| Outcome | Sample | Rate per 100 group-years, before / after | Rate ratio (95 % interval) |
|---|---|---|---|
| Start of targeted broad instrument (first hit) | Japan and Korea, 1962–1999 | 0.24 / 1.15 | 5.69 (2.31–14.02) |
| same, excluding Section 301 tariffs | China, 1992–2023 | 0.02 / 0.04 | 1.13 (0.11–11.24) |
| New US AD/CVD case | all, 1988–2015, controlling for export size | 3.38 / 6.48 | 1.10 (0.75–1.60) |
| same | all, without size control | 3.38 / 6.48 | 1.97 (1.37–2.82) |
| same | Japan, SITC Rev. 1, with size control | 3.62 / 12.00 | 2.01 (1.10–3.68) |

The Section 301 tariffs of 2018 covered all 813 Chinese HS groups at risk, displaced or not. AD and CVD cases from TTBD carry HS codes from 1988; they are matched to SITC groups through the WITS concordances HS 1988/92 to SITC Rev. 1 and Rev. 3. Weight (`data/population_weight.csv`): among displaced groups, the share with an AD or CVD case within five years of the crossover is 0.01, 0.11 and 0.30 by third of US imports from the challenger in the crossover year (N = 228); the share with a broad instrument within ten years (Japan and Korea, N = 66) is 0.27, 0.14 and 0.23. Employment (`data/population_employment.py`, `data/population_employment.txt`): US employment from the NBER-CES Manufacturing Industry Database (NAICS 1997, 1958–2018) in the crossover year (2018 for later years), allocated to groups by the share of each industry's HS10 import lines in the group (Census import concordance 2002; HS6 to SITC Rev. 1 through WITS). The share with an AD or CVD case within five years rises with employment by third (0.01, 0.16, 0.25; logit 0.43, p = 0.017), but the effect disappears once US imports from the challenger enter (0.11, p = 0.64; imports 0.33, p = 0.024). Broad instruments within ten years (Japan and Korea, N = 63): 0.19, 0.14 and 0.29 by third; logit 0.24 (p = 0.43). The allocation by number of tariff lines rather than value is an approximation.

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

A structural-break search on log(1 + mentions per 100,000 words), without imposing break dates, places the single best break in 1871 and, when two breaks are allowed, in 1871 and 1894, one year after the dye and the steel milestone respectively (BIC prefers one break over none by a wide margin; `data/tests_sequence.py`). Two qualifications follow. First, the rise after 1871 is modest in level; the large increase comes after 1894. Second, the competition indicator differs little between the absorption phase and the 1870s and 1880s, and the early annual values rest on very few debates. The parliamentary record therefore supports the ordering (attention follows displacement) but dates the escalation to the second, broader milestone.

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


Export data by sector sharpen the timing. Tyszynski (1951, Tables I and II) reports manufactured exports of eleven countries in sixteen groups for 1899 and 1913 (Table E6). In chemicals, German exports already exceeded British exports by 43 per cent in 1899, consistent with an early dye milestone. In iron and steel, by contrast, German exports were only 35 per cent of British exports in 1899 and reached 91 per cent by 1913; in industrial equipment and electrical goods Germany overtook Britain between the two benchmarks. The production crossover in steel (1893) thus preceded displacement in export markets, which came in the 1900s. The rise of German steel and machinery exports between 1899 and 1913 coincides with the period in which German competition became a parliamentary theme and Tariff Reform was launched (1903). Crafts (1989, Table 1) confirms the pattern from the side of specialisation: chemicals ranked among Germany's top five sectors of revealed comparative advantage in both 1899 and 1913, iron and steel did not (ranks 11 and 8), while electrical goods rose from rank 10 to rank 1.

**Table E6. German and American manufactured exports relative to British exports, by group (Britain = 1)**

| Group | Germany 1899 | Germany 1913 | United States 1899 | United States 1913 |
|---|---|---|---|---|
| Iron and steel | 0.35 | 0.91 | 0.27 | 0.39 |
| Chemicals | 1.43 | 1.70 | 0.52 | 0.44 |
| Industrial equipment | 0.50 | 1.33 | 0.59 | 0.75 |
| Electrical goods | 0.58 | 2.11 | 0.94 | 0.69 |
| All manufactures | 0.68 | 0.89 | 0.34 | 0.42 |

Source: Tyszynski (1951), Tables I and II, current £000; values transcribed from the scanned tables and checked against the text layer and against the country totals in Table VIII.

## E.7 Comparison: the United States

The United States overtook Britain in GDP per capita around 1900 (Maddison Project 2023). If displacement alone triggered escalation, British attention to the United States should rise as well. It does not. Mentions of the United States per 100,000 words of economic debate stay between 41 and 56 across all four periods (Germany: 14 rising to 43–45), and the share of debates linking the United States to competition terms stays near one per cent. Bilateral trade data support reading this as a scope condition rather than a refutation. In a fixed panel of 17 third markets with data for all three suppliers in every benchmark year from 1880 to 1913 (CEPII TRADHIST v4; Fouquin and Hugot 2016), German exports rise from 47 to 85 per cent of British exports and exceed them in seven markets by 1913 (Austria-Hungary, Belgium, Denmark, Finland, Italy, Norway, Sweden). US exports rise from 46 to 75 per cent, but to only 51 per cent once Canada is excluded, and exceed British exports only in Canada and Austria-Hungary (Table E5). The United States outgrew Britain at home; Germany displaced Britain in its export markets. A phrase search in the same debates finds no parliamentary echo of the press theme of an 'American invasion' around 1901: the phrase does not occur once in the 15,126 economic debates of 1850–1914, and 'American competition' occurs in six debates in all, against eleven for 'Made in Germany' (`data/hansard_phrases.py`). The primary claim locates the trigger in contested markets, and the British record is consistent with that.

**Table E5. Exports to 17 third markets relative to British exports (Britain = 1)**

| Year | United States | United States, without Canada | Germany |
|---|---|---|---|
| 1880 | 0.46 | 0.44 | 0.47 |
| 1890 | 0.30 | 0.25 | 0.50 |
| 1900 | 0.56 | 0.46 | 0.70 |
| 1913 | 0.75 | 0.51 | 0.85 |

Markets: Argentina, Austria-Hungary, Belgium, Canada, Chile, Denmark, Finland, France, British India, Italy, Japan, Norway, Ottoman Empire, Portugal, Spain, Sweden, Uruguay. Flows are total goods in current pounds and do not separate manufactures from primary goods.

For manufactures alone, Tyszynski's (1951, Table VIII) shares of world manufactured exports point the same way. Between 1899 and 1913 the British share fell from 32.5 to 29.9 per cent, the German share rose from 22.2 to 26.4 per cent, and the American share rose only from 11.2 to 12.6 per cent. Relative to Britain, Germany moved from 0.68 to 0.88, the United States from 0.34 to 0.42. In manufactured exports before 1914, Germany was closing on Britain; the United States was not.

## E.9 Further cases

The same rules as in E.4 are applied to eight further dyads. Code: `data/cases_fetch.py`, `data/cases_test.py` (output `data/cases_panel.txt`, `data/cases_breadth.csv`, `data/cases_crossovers.csv`, `data/cases_hazard.csv`, `data/cases_register_tested.csv`), `data/third_markets_1930s.py`, `data/hansard_japan.py`, `data/tests_sequence.py`.

**Data.** UN Comtrade, SITC Rev. 1 (1962–1999), SITC Rev. 3 (1992–2009), HS four-digit (2008–2023), world exports by reporter. Taiwan reports only in HS; for SITC its exports are the imports of all reporters from partner 490 ("Other Asia, nes"), compared with the same reporters' imports from the United States (both valued c.i.f.). Hong Kong: exports minus re-exports (re-exports by product only to 2016). Japan against Britain: CEPII TRADHIST v4, total bilateral exports, 35 markets with values for both suppliers in every year 1924–1938, without Japan's colonies.

**Table E7. Reach of displacement: share of American manufactured exports in groups the challenger had overtaken (challenger exports ≥ US exports and ≥ USD 50 million)**

| Challenger | Data | Selected years | Peak |
|---|---|---|---|
| Japan | SITC 1 | 0.31 (1977), 0.27 (1981), 0.35 (1987) | 0.48 (1995) |
| China | HS | 0.45 (2018) | 0.55 (2023) |
| Korea | SITC 1 / 3 | 0.024 (1977), 0.027 (1984), 0.024 (2002) | 0.074 (2009) |
| Taiwan | SITC 1 / 3 / HS | 0.011 (1977), 0.031 (1986), 0.087 (2023) | 0.095 (2005) |
| Vietnam | HS | 0.048 (2018), 0.064 (2023) | 0.064 (2023) |
| Mexico | HS | 0.066 (2023) | 0.083 (2022) |
| Malaysia | HS | 0.045 (2023) | 0.060 (2021) |
| Hong Kong | SITC 1 | 0.020 (1988) | 0.022 (1987) |
| Thailand | HS | 0.014 (2023) | 0.016 (2022) |
| Brazil | SITC 1 / HS | 0.007 (1984), 0.008 (2023) | 0.011 (2013) |

**Register.** Thirteen entries (B-24 to B-36 in `data/broad_register.csv`), each with its primary source: footwear OMA with Taiwan, June 1977 (Proclamation 4510); colour-television OMA with Taiwan, 1979 (Proclamation 4634); steel VRAs with Brazil and Mexico, 1984 (Moore 1996, Table 2.8); machine-tool VRA with Taiwan, 1987 (Dinopoulos and Kreinin 1991); 100 per cent tariffs on Brazilian goods, October 1988 (Proclamation 5885); GSP graduation of Hong Kong and Taiwan, 1989 (Proclamation 5805); US–Vietnam textile agreement, May 2003 (FR Doc. 03-12314); MFA/ATC quotas on Taiwan, Hong Kong, Thailand, Malaysia, Brazil and Mexico (in force 1994–2004 by Federal Register notices; start dates not verified, so excluded from the hazard); end of Hong Kong's differential treatment, 2020 (EO 13936); IEEPA tariffs on Mexico (EO 14194), all partners (EO 14257, 14326), Brazil (EO 14323) and Hong Kong (EO 14257), 2025. Six further entries (B-37 to B-42) date the first comprehensive US cotton textile agreement with each economy from Federal Register notices: Hong Kong (35 categories, from 1 October 1963), Taiwan (19 October 1963), Mexico (2 June 1967), Brazil (23 October 1970), Malaysia (1 September 1970; USITC Pub. 850, p. 50) and Thailand (16 March 1972). Earlier restraints on single categories (Hong Kong from 3 March 1962, Taiwan from 23 June 1962, Mexico from 10 August 1962, Brazil from October 1963, Malaysia from August 1966, Thailand requested April 1971) are recorded in the notes and scored IR 3. The MFA itself was done at Geneva on 20 December 1973 and entered into force on 1 January 1974 (Article 14(1); text reproduced in USITC Pub. 850, Appendix A).

**Table E8. Broad instruments against the further cases and the crossover of the groups they covered**

| Instrument | Target | IR | Crossover of covered groups | Phase |
|---|---|---|---|---|
| Footwear OMA 1977 | Taiwan | 4 | 1970 | post |
| Colour-TV OMA 1979 | Taiwan | 4 | none | extension of instrument against Japan |
| Steel VRAs 1984 | Brazil | 4 | 1983 | post |
| Steel VRAs 1984 | Mexico | 4 | none | extension |
| Machine-tool VRA 1986 | Taiwan | 4 | none | extension of instrument against Japan |
| Section 301 tariffs 1988 | Brazil | 4 | none | retaliation over patents |
| GSP graduation 1989 | Hong Kong, Taiwan | 4 (doubtful) | none (economy-wide) | rule-based |
| Cotton textile agreements 1963 | Hong Kong; Taiwan | 4 | 1965; 1971 | absorption (2 and 8 years) |
| Cotton textile agreements 1967–1972 | Mexico; Brazil; Malaysia; Thailand | 4 | none | restraint without displacement |
| Textile agreement 2003 | Vietnam | 4 | 2006 (apparel, SITC 84) | absorption (3 years) |
| HK differential treatment 2020 | Hong Kong | 5 | none | political |
| IEEPA tariffs 2025 | Mexico; Brazil; Hong Kong | 5 | none (economy-wide) | political |
| Reciprocal tariffs 2025 | all partners | 5 | none (economy-wide) | global, deficit-based |

**Hazard and control group.** Groups whose crossover is not in the first data year, and the share followed within ten years by a targeted sectoral broad instrument (without GSP graduation and without politically motivated measures): Taiwan SITC 1, 1 of 24; Brazil SITC 1, 4 of 9 (steel); Hong Kong SITC 1, 0 of 9; Vietnam SITC 3, 2 of 5 (apparel, quota of 2003 one year after the two groups crossed); Thailand, Malaysia, Mexico, Vietnam, Taiwan and Brazil in HS (2009–2023): 0 of 283. Panel of 3,702 group series: targeted sectoral broad instruments begin at 0.07 per 100 group-years before and 0.12 after the crossover (rate ratio 5.83, 95 % interval 2.84–11.95; year × source effects, clustered by group). With GSP graduation the ratio falls to 1.33 (1.07–1.65), because graduation covered all groups at once. AD/CVD cases (TTBD, 1988–2015) per 100 group-years rise from 0.97 to 1.98 after the crossover, but not once export size is held constant (rate ratio 1.29, 0.70–2.40), the same result as for Japan, Korea and China (E.4).

**Japan against Britain.** Milestone 1932 (British India import market, Hansard 4 July 1934: Japan 551.9, UK 541.9 million yards). Seven responses (`data/ds1_responses.csv`, R-JPGB-01 to 07), all checked at Historic Hansard; two before the milestone (economic mission 1930, IR 2; Indian differential duty 1930, IR 3), five from the milestone onwards, including all four with IR 4. These are reported separately and do not enter the core counts of 41 responses.

**Table E9. Japan against Britain: exports to third markets relative to Britain (TRADHIST) and parliamentary attention (Hansard)**

| Year | All 35 markets | Seven Asian markets | Netherlands Indies | British India | Mentions of Japan per 100,000 words |
|---|---|---|---|---|---|
| 1924 | 0.23 | 0.42 | 0.68 | 0.13 | 2.9 |
| 1929 | 0.30 | 0.58 | 0.99 | 0.23 | 1.7 |
| 1930 | 0.29 | 0.67 | 1.14 | 0.24 | 8.5 |
| 1932 | 0.32 | 0.67 | 2.12 | 0.42 | 12.4 |
| 1933 | 0.30 | 0.67 | 3.17 | 0.34 | 102.1 |
| 1934 | 0.31 | 0.75 | 3.88 | 0.39 | 44.0 |
| 1936 | 0.33 | 0.86 | 3.39 | 0.44 | 29.4 |
| 1938 | 0.27 | 0.71 | 1.88 | 0.33 | 16.5 |

The best single break in log(1 + mentions) is 1932 (BIC −11.2 against −0.1 without a break). In Ceylon, a colony that adopted quotas in 1934, the Japanese–British ratio fell from 0.50 in 1934 to 0.28 in 1935.

**Table E9b. Cotton piece goods and textile groups, Japan relative to Britain**

| Year | UK exports, million sq. yd (Robson 1957, p. 11) | UK exports, million linear yd (Robson, p. 333) | Japanese exports, million sq. yd (Sandberg 1974, Table 25, after Seki) | Japan / UK (square yards) |
|---|---|---|---|---|
| 1929 | 3,672 | 3,764.9 | 1,791 | 0.49 |
| 1931 | 1,716 | 1,790.2 | 1,414 | 0.82 |
| 1932 | – | 2,302.7 | 2,032 | (0.88 against linear yards) |
| 1933 | 2,031 | 2,116.7 | 2,090 | 1.03 |
| 1935 | 1,949 | 2,013.4 | 2,725 | 1.40 |
| 1937 | 1,922 | 2,023.1 | 2,644 | 1.38 |
| 1938 | 1,387 | 1,448.0 | 2,181 | 1.57 |

Imports into British India, million linear yards (Robson, p. 10): 1929 UK 1,276 / Japan 521; 1931 356 / 336; 1935 489 / 526; 1937 323 / 337; 1938 258 / 441. By value, Japanese exports of piece goods were 3 per cent of British exports in 1913, 31 per cent in 1928 and 73 per cent in 1935 (League of Nations 1945, p. 111). Tyszynski (1951), Tables III and IV (pp. 279–280), £000: textiles (group 12) UK 213,152 and Japan 60,446 in 1929, 121,782 and 65,888 in 1937 (ratio 0.28 and 0.54); apparel (group 13) 27,053 and 9,379 in 1929, 12,889 and 12,921 in 1937 (0.35 and 1.00). Japan's shares of the eleven-country totals (3.9 and 7.2 per cent) match Table VIII. Under the export rule (world crossover 1933), India's 50 per cent duty of August 1932 precedes the world crossover but follows the crossover in the Indian market (1932), the market it regulated. Data: `data/cotton_piece_goods_1913_1938.csv`, `data/tyszynski_1951_japan.csv`.

## E.10 Alignment, rivalry and the instruments available

Code: `data/geopolitics.py` (output `data/geopolitics.txt`, `data/geopolitics_instruments.csv`, `data/geopolitics_dyads.csv`); mode of each instrument in `data/geo_instrument_mode.csv`. Sources: ATOP 5.1 dyad-years 1815–2018 (Leeds et al. 2002), UN General Assembly ideal points 1946–2025, all votes (Bailey, Strezhnev and Voeten 2017; file of July 2025), Correlates of War National Material Capabilities v7, CINC 1816–2022. ATOP values after 2018 and CINC values after 2022 are carried forward. Taiwan has no UN votes after 1971; Hong Kong is not a state in these data. For the European Union, Germany stands in.

**Table E10. Form of targeted, trade-motivated broad US instruments by alliance and period (register, instrument–target pairs; global, politically motivated and undated instruments excluded; B-12 mixed and excluded)**

| Period | Defence pact with the US | Negotiated | Unilateral |
|---|---|---|---|
| before 1995 | yes (Japan, Korea, Taiwan to 1980, Brazil, Mexico, Thailand) | 21 | 4 (B-09, B-11, B-16, B-28) |
| before 1995 | no (Taiwan after 1980, Malaysia) | 2 | 1 |
| from 1995 | yes | 0 | 0 |
| from 1995 | no (China, Vietnam) | 1 (B-30) | 4 (B-20 to B-23) |

**Table E11. State of the dyad in the milestone years**

| Dyad | Capability ratio (CINC, challenger/incumbent) | UN ideal-point distance | Defence pact |
|---|---|---|---|
| Germany–Britain (1870–1900) | 0.44–0.79 | – | no |
| Japan–Britain (1932) | 0.59 | – | no |
| Japan–United States (1969–1987) | 0.26–0.40 | 1.1–1.6 | yes |
| Korea–United States (1992, 2000) | 0.15–0.16 | 2.0–2.4 | yes |
| China–United States (2010–2023) | 1.4–1.9 | 3.2–3.5 | no |

The only broad instrument before displacement, the export controls of October 2022 (IR 5), falls in the one dyad in which the challenger's composite capabilities exceeded the incumbent's (1.9) and the UN distance was largest (3.5). CINC weights population, energy and steel and thus overstates China's military weight relative to spending-based measures.

UN distance to the United States, mean 2009–2023: Japan 1.73, Korea 1.64, Mexico 2.53, Brazil 2.74, Thailand 2.90, Malaysia 3.12, China 3.30, Vietnam 3.40. Mexico (ally) and Vietnam (no ally) both displaced the United States in many HS groups and drew no targeted broad instrument before 2025.

**Table E12. Rules on the instruments available to the incumbent (WTO legal texts and accession records)**

| Date | Rule | Effect on the instruments |
|---|---|---|
| 1947 | GATT: Article VI (antidumping, countervailing duties), Article XIX (safeguards) | product remedies and safeguards legal; quantity limits only as exceptions |
| 1961–1962 | Short-Term and Long-Term Arrangements on cotton textiles | negotiated quotas on low-wage suppliers before displacement |
| 1 Jan 1974–1994 | Multifibre Arrangement (bilateral quotas, outside non-discrimination) | same, for all fibres |
| 1 Jan 1995 | WTO; Agreement on Safeguards, Article 11.1(b): no voluntary export restraints or orderly marketing arrangements | negotiated sectoral restraints outlawed; sectoral responses become AD/CVD and global safeguards |
| 1 Jan 1995 | TRIPS, TRIMs, Agreement on Subsidies | rules constrain the challenger's industrial policy (Wade 2003) |
| 1995–1 Jan 2005 | Agreement on Textiles and Clothing | MFA quotas phased out; ended 1 Jan 2005 |
| 11 Dec 2001 | China joins WTO (Chinese Taipei 1 Jan 2002) | China and Taiwan under WTO rules on safeguards |
| 11 Jan 2007 | Viet Nam joins WTO | US quotas on Vietnamese textiles and apparel eliminated with effect from 11 Jan 2007 (FR Doc. 07-65) |

Sources: WTO, Agreement on Safeguards (legal text 25-safeg.pdf); WTO, "Textiles: back in the mainstream" (texintro_e.htm); WTO, completed accessions (completeacc_e.htm); WTO, Viet Nam accession page. MFA: done at Geneva 20 December 1973, in force 1 January 1974 (Article 14(1)), Article 2(2)–(4) from 1 April 1974 (Article 14(2)); text as reproduced in USITC Pub. 850, Appendix A.

## E.11 Congressional attention: China 1995–2025, Japan and Korea 1955–1994

The Hansard measure (E.5, E.6) is repeated for the American incumbent with the Congressional Record, retrieved from the govinfo API of the US Government Publishing Office. Code: `data/crec_fetch.py`, `data/crec_filter.py`, `data/crec_salience.py`, `data/crec_sectors.py` (China); `data/crecb_fetch.py`, `data/crecb_salience.py` (Japan); `data/fr301_lists.py` (Section 301 lists); break tests in `data/tests_sequence.py`.

**China: data and filter.** The daily Congressional Record (collection CREC) is divided into granules, one per speech, debate or insertion, each with its own title. Of 829,186 granules from 1995 to 2025 (without the Daily Digest and front matter), 10,901 carry an economic title under a fixed filter (version `crec_econ_v1`: trade, tariff, import, export, duties, customs, manufacturing, industry, dumping, subsidy, competitiveness, currency, outsourcing, WTO, NAFTA, normal trade relations, supply chain, intellectual property and the sector terms of Table E14). China counts when *China*, *Chinese*, *PRC* or *Beijing* occurs; *Republic of China* (Taiwan) is removed first. The competition indicator uses the Hansard list plus *manipulation*, *overcapacity*, *outsourcing*, *offshoring* and *counterfeit*.

**Table E13. China in economic debates of the US Congress, pooled by period**

| Period | Economic granules | Mentioning China | China near a competition term | Mentions per 100,000 words: China / Japan / Mexico |
|---|---|---|---|---|
| 1995–2000 | 2,837 | 20.1 % [18.6–21.6] | 5.2 % [4.4–6.1] | 130 / 34 / 35 |
| 2001–2009 | 3,616 | 16.4 % [15.2–17.6] | 6.8 % [6.1–7.7] | 77 / 16 / 27 |
| 2010–2017 | 2,600 | 13.8 % [12.5–15.2] | 6.6 % [5.7–7.6] | 80 / 9 / 21 |
| 2018–2025 | 1,848 | 17.9 % [16.2–19.7] | 7.5 % [6.4–8.8] | 113 / 6 / 35 |

Brackets: 95 % Wilson intervals. Source: Congressional Record (govinfo, CREC). Figure E2 (`figures/fig_e2_crec.pdf`) shows the annual series.

Unlike Germany in the British record, China was a parliamentary subject before it displaced anyone. Its trade status was itself legislation: the annual renewal of most-favoured-nation treatment in the 1990s and permanent normal trade relations in 2000 (the peak of the series, 399 mentions per 100,000 words). Attention then falls back, with peaks in the currency debates of 2005 and 2011, and rises again after 2018. The competition indicator rises only slowly, from 5.2 to 7.5 per cent of economic granules. A break search on log(1 + mentions per 100,000 words) prefers no break (BIC); on the share of economic granules mentioning China it places two breaks in 2013 and 2018, a trough before the tariffs of 2018 rather than a rise after the crossovers, whose median falls in 2004 (SITC Rev. 3, 70 groups) and 2015 (HS, 242 groups). The aggregate record of Congress therefore does not show the British pattern of attention following displacement.

**Coverage of the title filter.** A check sample of ten random sitting days per year (310 days, 46,357 granules, all retrieved in full) measures what the filter misses. Of 259 granules in which China appears within 30 words of a competition term, 48 (19 per cent) carry an economic title; the others are bill introductions, appropriations and defence authorisations, nominations and amendment texts. Much of the economic discussion of China in Congress happens under non-economic titles, more than in the Victorian Parliament. The sample-day measure below therefore uses the full text of sampled days for both China and Japan.

**Table E14. China in congressional sector debates and broad American instruments, by sector**

| Sector | Crossover | Broad instrument (register) | China linked, before crossover | China linked, from crossover | Voice 2001–2017 | Share on 301 lists 1–2 | 301 increase 2024 |
|---|---|---|---|---|---|---|---|
| Steel | ≤1992 | B-17, B-19 | – | 17.4 % of 430 | 8.04 | 0.00 | yes |
| Aluminium | 2004 | B-19 | 11.1 % of 9 | 20.6 % of 34 | 0.32 | 0.03 | yes |
| Solar cells | ≤2008 | B-18 | 0.0 % of 19 | 25.9 % of 108 | 2.41 | 1.00 | yes |
| Washing machines | 1999 | B-18 | 0.0 % of 1 | 0.0 % of 4 | 0.00 | 0.00 | no |
| Telecom equipment | 2003 | B-21 | 5.4 % of 240 | 27.5 % of 160 | 1.61 | 0.00 | no |
| Semiconductors | 2009 | B-22 | 16.7 % of 60 | 42.2 % of 64 | 1.29 | 1.00 | yes |
| Cars | 2023 | B-23 | 20.6 % of 490 | 40.0 % of 40 | 11.26 | 0.87 | yes |
| Furniture | 2001 | – | 0.0 % of 17 | 34.1 % of 41 | 2.09 | 0.00 | no |
| Textiles and apparel | ≤1992 | – | – | 21.1 % of 294 | 7.72 | 0.00 | yes |
| Footwear | ≤1992 | – | – | 21.5 % of 93 | 2.25 | 0.00 | no |
| Toys | ≤1992 | – | – | 19.1 % of 89 | 2.25 | 0.00 | no |
| Tyres | 2005 | – | 12.0 % of 25 | 32.0 % of 25 | 1.29 | 0.07 | no |
| Paper | ≤2008 | – | 33.3 % of 3 | 20.0 % of 5 | 0.32 | 0.00 | no |
| Chemicals | 2004 | – | 12.6 % of 190 | 4.9 % of 144 | 1.93 | 0.01 | yes |
| Computers | 2003 | – | 11.4 % of 229 | 11.8 % of 153 | 4.50 | 0.20 | no |
| Glass and ceramics | ≤1992 | – | – | 4.6 % of 87 | 0.64 | 0.00 | no |
| Batteries | 2004 | – | 0.0 % of 15 | 32.4 % of 71 | 0.80 | 0.39 | yes |

Sector debate: economic granule with at least three sector terms; China linked: China within 30 words of a sector term. Crossover: earliest year in which Chinese world exports of a group in the sector reached American exports (data/population_crossovers.csv; ≤ marks a crossover in the first data year). Voice: China-linked sector debates per 1,000 economic granules, 2001–2017. Share on lists 1–2: mean share of the sector's HTS8 lines on Section 301 lists 1 and 2 (25 per cent from July and August 2018). Instruments from data/broad_register.csv without the economy-wide Section 301 tariffs (B-20). The 2024 increases for textiles and chemicals concern face masks and critical minerals.

**Tests, China.** (a) *Timing.* In the nine sectors with an uncensored crossover after 1999, China is linked to 14.0 per cent of 1,275 sector debates before the crossover [12.2–16.0] and 22.4 per cent of 732 debates from the crossover [19.5–25.6]; voice is higher after the crossover in four of nine sectors. Because attention to China in all debates also rises over time, this comparison does not separate displacement from trend. (b) *Selection.* Sectors that later received a sector-specific broad instrument had more China-linked debates than displaced sectors without one, but none of the differences is significant (exact one-sided permutation tests: voice 2001–2017 3.6 against 2.4, p = 0.25; five years before the crossover p = 0.43; five years from the crossover 4.8 against 1.4, p = 0.17). Import volume and employment do not separate the two groups either (p = 0.36 and 0.32). Counting the Section 421 tyre safeguard of 2009 and the textile safeguards of 2005 as broad instruments, which the register does not because they fall outside its Section 201 rule, changes little (p = 0.11 for voice 2001–2017). (c) *Graded tariffs.* The Section 301 tariffs of 2018 covered all groups, but not equally. Lists 1 and 2, the first to take effect at 25 per cent, concentrated on machinery, electronics, vehicles and plastics (Made in China 2025). Congressional voice does not predict a sector's share on lists 1 and 2 (Spearman ρ = 0.06, 17 sectors; among 229 displaced HS4 groups, OLS with 13 clustered sector groups, coefficient 0.06, p = 0.50 with import volume and employment held constant). It is weakly associated with the sector increases of the 2024 review (voice 4.2 against 1.7, p = 0.056).

The Section 301 lists come from the Federal Register: list 1, 83 FR 28710 (Annex A, 817 lines read); list 2, 83 FR 40823 (283); list 3, 83 FR 47974 (5,748); lists 4A and 4B, 84 FR 43304 (3,233 and 550); four-year review, 89 FR 76581 (Annex A, 387 of 389 lines; 11 of 14 product groups identified because three share lines with others). The counts differ by a few lines from USTR's totals because some codes also occur in the notes.

**Japan: data.** Before 1995 the Record exists in machine-readable form only as the bound edition (collection CRECB), one PDF with a text layer per sitting day and chamber, without debate titles. We draw 20 random sitting days per year from 1955 to 1994 (seed fixed in the code; 800 days, House, Senate and Extensions of Remarks) and read the full text (pdftotext). Without titles there is no economic filter: the measure counts the places where *Japan* or *Japanese* stands within 30 words of a competition term or a sector term, per million words of the whole day. For comparison the same measure is computed for China on the 310 check days of the daily Record (1995–2025). In all, 279 million words.

**Table E15. Japan and China near a competition term on sampled sitting days of Congress, per million words**

| Period | Japan, mentions per 100,000 words | Japan near a competition term | China near a competition term |
|---|---|---|---|
| 1955–1964 | 11.2 | 8.2 | 2.6 |
| 1965–1974 | 12.1 | 6.1 | 1.8 |
| 1975–1984 | 13.1 | 8.9 | 2.4 |
| 1985–1994 | 21.0 | 21.9 | 3.4 |
| 1995–2004 | 6.3 | 4.9 | 19.9 |
| 2005–2014 | 4.3 | 1.4 | 14.8 |
| 2015–2025 | 5.4 | 1.8 | 16.5 |

Japan as a competitor stays at a low, steady level through the 1960s and 1970s, when Japanese textiles, steel and television sets overtook American exports, and rises in the 1980s. A break search on log(1 + Japan near a competition term) places the single best break in 1980, the year of the car milestone (BIC −33.8 against −23.3 without a break); with two breaks, 1964 and 1980. The sample-day series for China prefers no break. On this common measure, congressional attention to China as a competitor after 1995 was of the same order as attention to Japan in the late 1980s, and it was already high in the first years of the series (PNTR, 2000), before most Chinese crossovers.

**Table E16. Japan in congressional sector debates and broad American instruments against Japan, by sector (sampled days, per million words)**

| Sector | Crossover (SITC Rev. 1) | Broad instrument (register) | Voice, five years before crossover | Voice, five years from crossover | Voice 1960–1975 |
|---|---|---|---|---|---|
| Textiles and apparel | ≤1962 | B-01, B-02, B-04 (from 1957) | 13.65 | 1.95 | 4.39 |
| Steel | ≤1962 | B-03, B-05, B-09, B-12, B-13, B-17 (from 1969) | 2.20 | 3.66 | 2.80 |
| Television sets | 1965 | B-07, B-16 (from 1977) | 0.63 | 0.41 | 0.88 |
| Cars and motorcycles | 1977 | B-10, B-11 (from 1981) | 1.16 | 5.69 | 1.26 |
| Semiconductors | 1989 | B-14, B-16 (from 1986) | 5.55 | 3.85 | 0.06 |
| Machine tools | 1977 | B-15 (from 1986) | 0.17 | 0.32 | 0.11 |
| Ships | ≤1962 | – | 0.47 | 0.24 | 0.48 |
| Footwear | ≤1962 | – | 0.21 | 0.62 | 0.71 |
| Cameras and optics | 1977 | – | 0.03 | 0.25 | 0.20 |
| Toys | ≤1962 | – | 0.21 | 0.10 | 0.09 |
| Glass and ceramics | ≤1962 | – | 0.63 | 0.43 | 0.55 |
| Ball bearings | 1986 | – | 0.00 | 0.11 | 0.01 |
| Tyres | 1969 | – | 0.16 | 0.12 | 0.13 |
| Plywood | ≤1962 | – | 12.07 | 0.14 | 0.22 |

Voice: places where Japan stands within 30 words of a sector term, per million words of the sampled days. Crossover: earliest year in which Japanese world exports in a group of the sector reached American exports (≤: in the first data year, 1962). Instruments from data/broad_register.csv.

**Tests, Japan.** The six sectors that drew a broad instrument against Japan had more congressional attention to Japan than the eight displaced sectors that did not: in the five years from the crossover 2.65 against 0.25 per million words (exact one-sided permutation test, p = 0.004), in the fixed window 1960–1975 1.58 against 0.30 (p = 0.022). In the five years before the crossover the difference is smaller and not significant (3.89 against 1.72, p = 0.17), and it rests on textiles and plywood, both debated in the late 1950s; in textiles the first restraint (1957) preceded the crossover. Voice rises after the crossover in four of the seven sectors with an uncensored crossover. These counts do not adjust for sector size; Table E18 does, and the difference then rests on how much Congress debates a sector, not on how often it names Japan.

**Korea: data and tests.** The same 1,110 sampled sitting days are read for Korea (`data/crecb_korea.py`). Mentions that do not refer to the South Korean economy are removed first: *North Korea(n)*, *Democratic People's Republic of Korea*, *Korean War*, *Korean conflict*, *Korean peninsula*. Korea counts at *Korea*, *Korean(s)*, *Korea's* and *Seoul*. Korea near a competition term rises from 0.7 per million words in 1955–1964 to 1.2 in 1975–1984 and 2.6 in 1985–1994, about a tenth of the level for Japan, and peaks at 6.8 in 2005–2014, the years of the bilateral free trade agreement; a break search prefers no break.

**Table E17. Korea in congressional sector debates and broad American instruments against Korea, by sector (sampled days, per million words)**

| Sector | Crossover (SITC Rev. 1 or 3) | Broad instrument (register) | Voice, five years before crossover | Voice, five years from crossover | Voice 1965–1990 |
|---|---|---|---|---|---|
| Textiles and apparel | 1970 | B-02, B-04 (from 1962) | 0.15 | 1.26 | 0.83 |
| Footwear | 1972 | B-06 (from 1977) | 0.00 | 0.17 | 0.23 |
| Television sets | ≤1992 | B-08 (from 1979) | 0.51 | 0.12 | 0.25 |
| Steel | 1977 | B-13, B-17, B-19 (from 1984) | 0.30 | 0.18 | 0.38 |
| Washing machines | 2002 | B-18 (from 2018) | 0.00 | 0.00 | 0.01 |
| Ships | 1977 | – | 0.11 | 0.14 | 0.10 |
| Telecom equipment | 2003 | – | 0.06 | 0.07 | 0.12 |
| Plywood | 1968 | – | 0.00 | 0.00 | 0.00 |
| Leather | ≤1992 | – | 0.00 | 0.00 | 0.05 |
| Travel goods | 1974 | – | 0.00 | 0.06 | 0.01 |
| Glass and ceramics | 1979 | – | 0.11 | 0.08 | 0.08 |
| Toys | 1985 | – | 0.00 | 0.00 | 0.01 |
| Copper, zinc, nickel | 1988 | – | 0.00 | 0.00 | 0.03 |
| Optical goods | 1991 | – | 0.07 | 0.04 | 0.04 |

The five displaced sectors that drew a broad instrument against Korea had more congressional attention to Korea than the nine that did not, in every window: 0.34 against 0.05 per million words in 1965–1990 (exact one-sided permutation test, p = 0.004), 0.19 against 0.04 before the crossover (p = 0.047) and 0.35 against 0.04 from the crossover (p = 0.016). Unlike Japan, the difference already appears before displacement, consistent with the instruments against Korea in textiles and television sets that preceded or extended restraints aimed at Japan (E.9). These counts, too, do not adjust for sector size (Table E18).

**Table E18. Size-adjusted congressional measures: sector volume and the challenger's share of it (sampled days)**

| Challenger | Sector | Broad instrument | Sector volume, five years before crossover | Sector volume, five years from crossover | Challenger share, before (%) | Challenger share, from (%) |
|---|---|---|---|---|---|---|
| Japan | Textiles and apparel | yes | 309.9 | 203.9 | 5.5 | 1.2 |
| Japan | Steel | yes | 91.9 | 66.2 | 2.4 | 5.2 |
| Japan | Television sets | yes | 92.3 | 104.9 | 0.4 | 0.5 |
| Japan | Cars and motorcycles | yes | 131.0 | 88.8 | 0.9 | 5.6 |
| Japan | Semiconductors | yes | 34.1 | 18.0 | 17.2 | 18.9 |
| Japan | Machine tools | yes | 4.2 | 2.3 | 3.9 | 6.3 |
| Japan | Ships | no | 22.0 | 20.8 | 2.4 | 0.7 |
| Japan | Footwear | no | 10.2 | 18.3 | 2.0 | 3.1 |
| Japan | Cameras and optics | no | 11.0 | 8.0 | 0.2 | 3.1 |
| Japan | Toys | no | 2.3 | 1.9 | 7.0 | 5.1 |
| Japan | Glass and ceramics | no | 31.0 | 20.5 | 2.2 | 1.9 |
| Japan | Ball bearings | no | 1.1 | 1.0 | 0.0 | 7.4 |
| Japan | Tyres | no | 28.6 | 34.3 | 0.3 | 0.4 |
| Japan | Plywood | no | 33.4 | 5.1 | 43.4 | 0.9 |
| Korea | Textiles and apparel | yes | 132.0 | 121.9 | 0.1 | 1.5 |
| Korea | Footwear | yes | 22.4 | 17.5 | 0.0 | 0.8 |
| Korea | Television sets | yes | 99.8 | 135.9 | 0.4 | 0.1 |
| Korea | Steel | yes | 51.4 | 76.5 | 0.5 | 0.3 |
| Korea | Washing machines | yes | 6.0 | 7.5 | 0.0 | 0.0 |
| Korea | Ships | no | 11.4 | 18.7 | 0.7 | 1.0 |
| Korea | Telecom equipment | no | 62.0 | 34.2 | 0.1 | 0.4 |
| Korea | Plywood | no | 6.2 | 3.8 | 0.0 | 0.0 |
| Korea | Leather | no | 3.2 | 2.2 | 0.0 | 0.0 |
| Korea | Travel goods | no | 1.7 | 1.1 | 0.0 | 5.1 |
| Korea | Glass and ceramics | no | 18.9 | 13.3 | 0.6 | 0.6 |
| Korea | Toys | no | 4.3 | 7.3 | 0.0 | 0.0 |
| Korea | Copper, zinc, nickel | no | 12.8 | 9.0 | 0.0 | 0.0 |
| Korea | Optical goods | no | 11.2 | 14.6 | 0.6 | 0.3 |

Sector volume: mentions of the sector terms per million words of all sampled days. Challenger share: per cent of those mentions with Japan (Korea) within 30 words (`data/crecb_share.py`, `data/ds1_share_test.txt`).

**Size adjustment.** The counts in Tables E16 and E17 mix two things: how much Congress talks about a sector, and how much of that talk names the challenger. Table E18 separates them. The challenger's share of sector talk does not separate the sectors that drew a broad instrument from those that did not, neither for Japan (from the crossover 6.3 against 2.8 per cent, exact one-sided permutation test p = 0.11; before 5.0 against 7.2 per cent, p = 0.51) nor for Korea (p = 0.48 and 0.59). Sector volume does, and already before displacement: in the five years before the crossover, Congress mentioned the Japanese sectors that later drew a broad instrument 111 times per million words, the others 17 times (p = 0.006); for Korea 62 against 15 (p = 0.020); from the crossover p = 0.010 for both. The differences in Tables E16 and E17 therefore reflect sector volume. What selects displaced sectors for broad constraint is the political weight of the sector at home, measured by how much Congress debates it before displacement, not attention to the particular challenger. This is the Hansard definition of voice (E.6: the number of debates on a sector). The sector terms differ in breadth (*television* also covers broadcasting, *cars* also railway cars), which inflates the volume of some large sectors; the ordering does not rest on them alone, since textiles and steel lead in both cases. For China, the number of economic debates on a sector (Table E14) does not separate significantly (237 against 148 debates, p = 0.15), nor does the share linking China (25 against 20 per cent from the crossover, p = 0.22).

**Controls for employment and imports.** Sector volume is correlated with the size of the American industry (Spearman 0.38 with employment, 0.24 with imports from the challenger). We therefore regress the indicator for a broad instrument on log sector volume before the crossover, log American employment and log American imports from the challenger in the crossover year, with a country indicator (`data/crecb_controls.py`, `data/ds1_share_controls.txt`). Employment and imports are computed for every displaced group, including those that crossed in the first data year, by the rules of the population check (NBER-CES employment distributed to groups through the Census concordance of 2002, before 1958 at its 1958 level; UN Comtrade imports); for the 79 groups already in data/population_weight.csv the values match exactly. All 28 sectors enter (Japan 14, Korea 14; 11 with a broad instrument). Alone, volume (coefficient 0.22 per log point, permutation p = 0.002), employment (0.18, p = 0.009) and imports (0.11, p = 0.007) each predict a broad instrument. Together, volume keeps most of its coefficient (0.18, permutation p = 0.011, 10,000 draws within country), employment loses its (p = 0.33) and imports keep a smaller, borderline one (0.08, p = 0.084). At the level of the 63 displaced groups, with the sector's instrument as outcome and standard errors clustered by sector, the result is the same (volume p = 0.021, employment p = 0.75, imports p = 0.40). Congressional volume thus carries information that the size of the industry and its exposure to imports do not.

**Limits of the congressional measures.** The sample of days is small for sector counts in single years; the text layer of the bound Record contains OCR errors and runs adjacent columns together, which blurs the 30-word window, though the share of common function words is similar in 1958, 1970 and 1985 (0.30, 0.29 and 0.28 of all tokens in five days each), so the noise does not appear to change over time; the daily Record's title filter misses most economic discussion of China (above); and the voice measures count attention to the challenger in a sector, not lobbying or votes.


## E.12 Multilateral finance: IMF conditions, aid and the Security Council

Code: `data/conditionality.py` (output `data/conditionality.txt`, `data/conditionality_challengers.csv`). Data: replication files of Stubbs, Reinsberg, Kentikelenis and King (2020; Harvard Dataverse doi:10.7910/DVN/YSZ79K), country-years 1989–2014, binding IMF conditions (quantitative and structural performance criteria plus prior actions) coded by policy area as in Kentikelenis, Stubbs and King (2016), temporary Security Council membership and voting similarity with the United States; and of Stubbs, Kentikelenis and King (2016; doi:10.7910/DVN/TE8TXZ), US ODA commitments 1980–2011 (OECD DAC) with the Security Council data of Dreher, Sturm and Vreeland. Programme years without coded conditions (for example Thailand 1997–2000) are treated as missing.

**Table E15. Binding IMF conditions per programme year (Poisson, year effects, errors clustered by country; 1,173 programme years, 116 countries)**

| Outcome (mean) | Security Council seat | Voting similarity with the US (0–1) | Same, with country effects: seat / similarity |
|---|---|---|---|
| All binding conditions (26.0) | 1.00 (p = 0.98) | 1.83 (p = 0.009) | 1.00 / 0.59 (p = 0.97 / 0.20) |
| External sector (2.8) | 1.08 (p = 0.67) | 2.05 (p = 0.12) | 1.13 / 1.05 |
| Financial sector (6.3) | 0.76 (p = 0.009) | 1.61 (p = 0.23) | 0.85 / 0.58 |

Rate ratios; controls: log GDP per head, growth, trade openness. Programme participation (logit, 4,001 country-years): similarity +3.14 (p = 0.001), seat +0.27 (p = 0.17). US aid commitments, log(1 + USD million), country and year effects, 3,257 country-years: seat −0.02 (p = 0.82), similarity +1.07 (p = 0.045), defence pact −0.58 (p = 0.43).

The challengers of this paper (Mexico, Korea, Brazil, Vietnam; Thailand without coded conditions; Malaysia and China without programmes) had 0.99 times as many binding conditions as other programme countries but 2.16 times as many on the external sector (p = 0.009). Their programmes began after financial crises, when the groups they had overtaken held at most 2.3 per cent of American manufactured exports.

## E.8 Limitations

1. **Second coder.** All IR scores currently come from one coder. Inter-coder agreement (Krippendorff's α, ordinal) will be reported here.
2. **Congressional check.** The daily Congressional Record (1995–2025) is measured in full under a title filter; before 1995 only a sample of 20 sitting days per year of the bound Record (1955–1994) is used (E.11).
3. **Milestone sources.** The Japanese steel milestone (1969, largest exporter) rests on a single secondary source; the voluntary restraint arrangement took effect in the same year (lag 0). Several Chinese milestones depend on the chosen measure (telecom equipment: revenue 2012 or equipment sales 2017).
4. **Title filter.** Economic debates are identified by title. Debates on economic matters under other titles, for example within question time, are missed. In the Congressional Record the filter captures only 19 per cent of granules in which China appears near a competition term (E.11).
5. **Register rule.** The register includes Section 201 safeguards only if they ended in quantity limits or orderly marketing agreements. The China-specific Section 421 tyre safeguard of 2009 and the textile safeguards of 2005 are therefore not in it; counting them changes the congressional sector test little (E.11).

## References

Crafts, N. F. R. (1989) 'Revealed comparative advantage in manufacturing, 1899–1950', *Journal of European Economic History*, 18(1), pp. 127–137.


Fouquin, M. and Hugot, J. (2016) *Two Centuries of Bilateral Trade and Gravity Data: 1827–2014*. CEPII Working Paper No. 2016-14. Paris: CEPII.

Tyszynski, H. (1951) 'World trade in manufactured commodities, 1899–1950', *The Manchester School*, 19(3), pp. 272–304. doi:10.1111/j.1467-9957.1951.tb00012.x
