# Displacement Before Escalation — Project Handover State

## State of Play
1. The manuscript "Displacement Before Escalation: Technology Acquisition, Incumbent Response, and Convergence Limits in Four Late-Industrialising Economies" is content-complete and targeted at *World Development* (Elsevier; desk rejection rate near 75%, overall acceptance near 10%); it has passed initial drafting, German-language peer review, style-guide application, LaTeX conversion, and a final reframing toward development political economy.
2. The empirical backbone consists of five structured datasets (DS1–DS5); four (DS2–DS5) are reproducible from public institutional databases at high confidence, while the event dataset (DS1) is medium-confidence because one required component — the absorption-phase salience table cited as Appendix E — is asserted in the manuscript but not yet populated.
3. The single blocking task before submission is populating Appendix E: without absorption-phase salience scores, the primary claim's defence against a circularity objection is unevidenced, and a referee request for that table would expose the gap.
4. Three secondary data issues are open but non-blocking: two US–Japan Section 301 cases remain unconfirmed in public USTR records, China's total factor productivity (TFP) values after 2019 are not yet extracted, and Germany is absent from the basic-research comparison because the required OECD sector breakdown is unavailable.
5. Three additional index projects (press-discourse, policy-action, policy-amnesia) are fully architected with working pipeline infrastructure but contain no collected data; they constitute a distinct second-phase project, not inputs the current manuscript depends on.

## Central Argument and Cases

The paper advances three hierarchically ordered claims, tested comparatively across four catch-up episodes benchmarked against the United States productivity frontier: Germany (1840–1914), Japan (1950–1990), South Korea (1960–1997), and China (1978–2024).

**Primary claim — displacement precedes escalation.** Incumbent powers escalate rhetoric and impose binding trade restrictions primarily *after* measurable technological displacement in contested sectors, not in response to adjudicated legal violations and not pre-emptively. This is a within-case sequencing regularity — establishing temporal order, not econometric causation — and it holds across all four cases and all coding variants examined.

**Secondary claim — convergence ceiling.** Convergence in GDP per capita and TFP decelerates and stalls at roughly 60–75% of the US frontier. Japan is the clearest instance: TFP peaked near 0.68 of the US level around 1991 and has since fallen to approximately 0.64 (relative to US = 1.0). South Korea plateaued near 0.66 TFP after around 2010–2012. Germany is the sole full-convergence exception, with TFP at or above US parity; its remaining GDP-per-capita gap reflects labour-supply structure rather than a productivity shortfall. China remains below the ceiling zone at roughly 33% of US GDP per capita, with its growth differential over the US narrowing from about 6 percentage points annually (2000–2010) to about 2 points since 2015.

**Exploratory claim — basic-research lag.** The timing of convergence deceleration is consistent with a 15–25 year lag between shifts in basic-research intensity and frontier-productivity outcomes. This is asserted from cross-case timing inspection, not estimated; it is framed explicitly as post-hoc and small-N constrained, and the manuscript is deliberately structured so that the primary claim stands independently of whether this interpretation holds.

The design's theoretical positioning draws on five literatures: developmental-state theory (Johnson, Amsden, Wade, Evans), the convergence and growth literature (Baumol; Acemoglu, Aghion and Zilibotti; Eichengreen, Park and Shin), trade-policy political economy (Irwin; Bayard and Elliott), the technology-denial literature (Nelson; Mowery), and intellectual-property norm-change history (Lerner; Moser; Murmann). For *World Development*, China is framed as a large late-industrialising economy under external constraint rather than a sui generis geopolitical rival.

## The Five Datasets

| ID | Content | Source | Structure | Status | Principal gap |
|---|---|---|---|---|---|
| DS1 | Displacement milestones and incumbent-response events, with Manifest Salience Score (MSS, 1–5 ordinal intensity scale) | Primary sources and secondary literature, manually coded | Dyadic event list, ~80 events | Partial — Appendix E rows empty | Absorption-phase instruments not yet scored |
| DS2 | GDP per capita, ratio to US | Maddison Project Database 2023 | Annual long-run series, 4 countries + US | Substantial | China pre-1952 values are low-reliability estimates |
| DS3 | TFP relative to US | Penn World Tables 11.0 (RTFPNA) | Annual panel 1950–2019 | Partial | Coverage ends 2019; China post-2019 requires Conference Board Total Economy Database supplement |
| DS4 | Basic-research intensity (share of gross domestic R&D expenditure and of GDP) | OECD Main Science and Technology Indicators | Annual panel, three countries | Partial | Germany sector breakdown unavailable in OECD source; comparison is three-country |
| DS5 | Technology balance of payments — licensing receipts, payments, balance | World Bank balance-of-payments data; OECD | Annual series 1970–2023 | Substantial | Pre-1970 values reconstructed from secondary sources; no pre-1970 primary series |

Normalisation is consistent within each series: TFP and GDP per capita are expressed relative to the contemporaneous US level; technology balance of payments is reported in absolute USD and as a share of GDP. No interpolation or smoothing is applied beyond values already published by the primary sources.

## Verified Historical Corrections Carried Into the Datasets

Several factual points were settled during the project and must be reflected in DS1 event coding. The German–British steel growth differential is roughly 9% versus 3.3% annually, not 6% versus 1%. Germany's share of the world synthetic-dye market reached approximately 75–80% by 1914, not 90%; Britain never held around 50% alone, sharing early dominance with France until about 1864. The 1989 global semiconductor ranking was NEC–Toshiba–Hitachi. Samsung achieved the world's largest DRAM market share in 1992; in its earlier technology acquisition, Micron supplied the DRAM design while Sharp's contribution concerned SRAM and ROM rather than DRAM. The US Section 301 investigation of China was initiated on 18 August 2017 (the 24 August date is the Federal Register publication). The leather-trade Section 301 case against Japan was initiated in 1977, not 1982, which affects annual case counts. WTO dispute DS594 was filed on 31 January 2020.

## The Open Vulnerability — Appendix E

The primary claim asserts that binding escalation systematically post-dates displacement. A referee can object that this is circular unless absorption-phase responses — incumbent actions during the period *before* the challenger became a genuine competitor — are shown to carry systematically lower salience than displacement-triggered escalation. The manuscript makes exactly this comparison in its results and setup sections and attributes it to Appendix E. Appendix E does not yet exist as a written table. If a referee requests it and any absorption-phase instrument scores MSS ≥ 4 before a displacement milestone, the circularity defence weakens materially. Populating Appendix E requires coding all absorption-phase policy instruments across the four cases for MSS and, as a prerequisite, defining the absorption-phase boundary explicitly (for example, the pre-displacement-milestone window or a fixed initial span of each catch-up episode), which is currently left implicit.

## Known Fragilities Beyond Appendix E

The 60–75% ceiling is a pattern drawn from four cases, not a statistically estimated threshold; the regression-to-mean interpretation (Pritchett and Summers 2014) is observationally equivalent for this sample and is acknowledged rather than formally rejected. The basic-research lag has no estimated coefficient or confidence interval. Germany's exceptional full convergence is attributed to its institutional basic-research infrastructure (Max Planck, Helmholtz, Leibniz, Fraunhofer), but the causal identification is not established. The MSS scoring rubric and inter-coder reliability protocol are not fully documented in reproducible form. China's TFP deceleration appears to begin before it enters the hypothesised ceiling zone — an anomaly that must be framed explicitly in the text rather than left silent, since it partially cuts against the ceiling interpretation.

## Adjacent Assets — Researched, Not Integrated

Substantial supporting research is complete but sits outside DS1–DS5. A newspaper panel for the United Kingdom, United States, France, and Germany across five historical periods has been identified, with nine archives audited for reproducibility and OCR quality assessed for the British Newspaper Archive, Chronicling America, and Gallica. Inventories of historical patent data (1850–1930) and digitised primary sources on "technology theft" rhetoric (1850–1914) are complete. Thailand and Vietnam have been assessed as robust non-convergence control cases that did not trigger technology-theft rhetoric, with data availability confirmed in Penn World Tables and the APO Productivity Databook. A 57-entry annotated bibliography on IP norm change is finished. Three index projects — a press-discourse index, a trade-normalised policy-action index (with a four-script Python pipeline that passes a synthetic smoke test), and a policy-amnesia index — are architected but hold no real data. None of these are required for the current manuscript; the control cases and the newspaper-based work are the most natural extensions.

## Priority Sequence to Submission

The blocking step is populating Appendix E with absorption-phase MSS scores and an explicit absorption-phase definition. Next, resolve the two unconfirmed Section 301 cases against Japan — the minimum viable fix is to footnote them as reported by Bayard and Elliott (1994) but not independently verified, and to recount annual totals accordingly. Then extract China's TFP directly from Penn World Tables 11.0 and splice Conference Board Total Economy Database values for 2020 onward, documenting the join. Strategically, integrating Thailand and Vietnam as explicit negative controls in the manuscript would strengthen the falsification logic using material that already exists, and sourcing Germany's basic-research breakdown from Federal Ministry of Education and Research annual reports or institutional budgets would make the basic-research comparison symmetric across all four cases.

## References

Acemoglu, D., Aghion, P. and Zilibotti, F. (2006) 'Distance to frontier, selection, and economic growth', *Journal of the European Economic Association*, 4(1), pp. 37–74.

Bayard, T.O. and Elliott, K.A. (1994) *Reciprocity and Retaliation in U.S. Trade Policy*. Washington, DC: Institute for International Economics.

Conference Board (2025) *Total Economy Database*. New York: The Conference Board.

Eichengreen, B., Park, D. and Shin, K. (2012) 'When fast-growing economies slow down: international evidence and implications for China', *Asian Economic Papers*, 11(1), pp. 42–87.

Feenstra, R.C., Inklaar, R. and Timmer, M.P. (2021) *Penn World Table version 11.0*. Groningen Growth and Development Centre, University of Groningen.

Irwin, D.A. (1996) 'The US–Japan semiconductor trade conflict', in Krueger, A.O. (ed.) *The Political Economy of Trade Protection*. Chicago: University of Chicago Press.

Lerner, J. (2002) *150 Years of Patent Protection*. NBER Working Paper No. 7478. Cambridge, MA: National Bureau of Economic Research.

Maddison Project (2023) *Maddison Project Database 2023*. Groningen Growth and Development Centre, University of Groningen.

Moser, P. (2005) 'How do patent laws influence innovation? Evidence from nineteenth-century world's fairs', *American Economic Review*, 95(4), pp. 1214–1236.

Murmann, J.P. (2003) *Knowledge and Competitive Advantage: The Coevolution of Firms, Technology, and National Institutions*. Cambridge: Cambridge University Press.

Pritchett, L. and Summers, L.H. (2014) *Asiaphoria Meets Regression to the Mean*. NBER Working Paper No. 20573. Cambridge, MA: National Bureau of Economic Research.
