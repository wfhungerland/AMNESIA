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

DS1 contains 16 sectoral milestones and 39 incumbent responses across the four cases (files `ds1_milestones.csv`, `ds1_responses.csv`, `ds1_events.csv`). Each row cites its source. For Japan, three sectors with disputes before 1980 were added to avoid an artificially empty absorption phase: cotton textiles (milestone 1951), colour television (1970) and steel (1969).

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

## E.6 Limitations

1. **Second coder.** All MSS scores currently come from one coder. Inter-coder agreement (Krippendorff's α, ordinal) will be reported here.
2. **Parliamentary check only for Britain.** Machine-readable full text of the US Congressional Record before 1994 is not openly available; the Japanese and Korean cases rest on the coded instruments alone.
3. **Milestone sources.** The Japanese steel milestone (1969, largest exporter) rests on a single secondary source; the voluntary restraint arrangement took effect in the same year (lag 0). Several Chinese milestones depend on the chosen measure (telecom equipment: revenue 2012 or equipment sales 2017).
4. **Title filter.** Economic debates are identified by title. Debates on economic matters under other titles, for example within question time, are missed.
