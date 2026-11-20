# Anti-Catch-up Rhetoric in Incumbent-Economy Press: Conceptual, Source-Critical and Measurement Foundations for a Dyadic, Country-Decomposable Long-Run Index (1870–present)

*Verified version v1 (2026-08-10). Corrections from verify round 1 are incorporated inline; items that could not be checked against an accessible primary source this round are marked [nicht prüfbar].*

## A. Executive Summary

This report assesses the feasibility of constructing a reconstructible, dyadically resolved, cross-epoch index of five anti-catch-up rhetoric frames in incumbent-economy media, spanning UK→Germany (1870–1914), USA→Japan and EC/EU→Japan (1965/70–1995), and USA/Germany/France→China (1995–present). The central conclusion is **qualified feasibility**: the conceptual apparatus (Entman-style framing plus a supervised, anchor-based hybrid measurement model) is sound and the five frames are largely defensible, but the index cannot be built as a single, uniformly comparable instrument across all dyads. It is realistically a **tiered instrument** — robust and confirmatory for some dyad-epochs, merely exploratory for others — because the underlying archival infrastructure is radically uneven in coverage, access mode, OCR quality, and language.

Five hard restrictions dominate. First, **frame non-orthogonality**: the security and technology-appropriation frames overlap heavily (espionage is simultaneously a security threat and a technology-transfer claim), and the systemic-ideological frame is near-absent in the UK→Germany dyad, where the rivalry was liberal-imperial rather than ideological. H1 (five cleanly separable frames stable across all dyads) is therefore **partially falsified**: the frames are separable analytically but empirically entangled, and at least one frame collapses in at least one dyad. Second, **semantic drift and non-existence of anchors**: several contemporary anchors ("forced technology transfer", "social dumping", "systemic rival") did not exist as lexicalized concepts before their epoch, so cross-epoch anchor lexica must be epoch-specific and mapped, not shared. H2 (historical continuity of anchors) survives, but only via curated, epoch-specific equivalence tables rather than a single fixed lexicon. Third, **archival asymmetry**: high-quality, programmatically queryable, persistent-ID full-text archives exist in dense continuity for the UK→Germany (Times Digital Archive), USA→Japan/China (ProQuest Historical Newspapers; Chronicling America to 1963), and French (Gallica/RetroNews) cases, but the German press panel has a structural discontinuity — ZEFYS/Deutsches Zeitungsportal cover roughly 1671–1950 while the crucial post-1990 German China-debate lives in commercial archives (Spiegel, Zeit, FAZ, Handelsblatt) with restrictive licensing and no bulk full-text access. H3 (uniformly dense machine-readable archives per dyad) is therefore **falsified for the German dyad's post-1990 window and for the EC/EU institutional-plus-press panel**. Fourth, **volume-versus-tone confounding**: raw frame frequency conflates how much a target is discussed with how hostile the coverage is, requiring explicit exposure normalization. Fifth, **classifier drift**: a supervised model trained on one epoch's language degrades on another, mandating epoch-stratified training and validation.

The recommended design is a two-layer hybrid: (Layer 1) anchor-based, per-100,000-word-normalized frame frequencies with epoch-specific lexica; (Layer 2) a supervised multilingual transformer classifier trained on a stratified, manually labeled sample, storing per-article, per-frame probabilities. Three indices follow: FrameIntensity (mean predicted probability), SalienceIndex (target-related economic articles / all economic articles of the incumbent-country-year), and OverallIndex (mean across frames). The index is publication-worthy as a **comparative-historical instrument with explicit tiering and uncertainty flags**, not as a single seamless time series.

## B. Frame Validation Against the Framing Literature

The frames should be grounded in the dominant paradigm of media framing, Entman's (1993, p. 52) canonical definition: "To frame is to select some aspects of a perceived reality and make them more salient in a communicating text, in such a way as to promote a particular problem definition, causal interpretation, moral evaluation, and/or treatment recommendation for the item described." Entman himself characterized framing as a "fractured paradigm" (1993, p. 51), and this fracturing is analytically useful here: it licenses a *deductive, issue-specific* frame catalogue rather than a purely inductive one.

Three competing operationalizations of "frame" are relevant. (1) **Framing theory / content analysis** (Entman 1993; Gitlin 1980; Gamson & Modigliani 1989; the Policy Frames Codebook of Boydstun & Gross 2014 operationalized in the Media Frames Corpus of Card et al. 2015) treats frames as latent organizing ideas identified through human-coded exemplars. (2) **Topic modeling** (LDA and dynamic LDA) discovers co-occurrence clusters inductively but is notoriously corpus-specific and tends to conflate *topic* with *frame* — the well-known critique that the Media Frames Corpus's broad "Economic" dimension mixes issue and frame. (3) **Stance detection** identifies the author's position (for/against a target) rather than the interpretive schema, and is a narrower task.

The correct choice for a reconstructible instrument is an **anchor-based supervised hybrid** that sits between framing theory and supervised classification: deductive frame definitions (from theory and historical discourse) anchor a lexicon that seeds a supervised classifier, whose predictions are then validated against human labels. This is the direction of the computational-framing literature, which finds that deductive control must be injected either as theory-justified keywords or as a fully coded training set, and that supervised transformer models fine-tuned on coded data outperform both LDA and lexical baselines while remaining explainable when grounded lexically. The hybrid preserves reconstructibility because both the seed lexicon and the labeled sample are storable, inspectable artifacts.

**Discriminant validity of the five frames.** Applying the Policy Frames Codebook lens, the five proposed frames map onto recognized dimensions but are not mutually exclusive:
- *Security / strategic threat* ≈ PFC "Security and defense" — robust and cross-epoch stable.
- *Unfair competition / rule-breaking* ≈ PFC "Fairness and equality" + "Economic" — robust but broad.
- *Systemic-ideological conflict* ≈ PFC "Political" / "Cultural identity" — **weakest cross-dyad**; strong for USA→China (Cold-War-inflected) and EC→Japan ("Japan Inc."/model competition), largely absent for UK→Germany.
- *Deindustrialization / employment threat* ≈ PFC "Economic" + "Quality of life" — robust in all four dyads.
- *Technology appropriation / espionage* — **overlaps structurally with Security**; espionage claims are jointly a security and an appropriation claim.

The strongest internal threat to H1 is therefore the collapse of the technology-appropriation frame into the security frame, and the near-emptiness of the systemic-ideological frame in the earliest dyad. The design response is to keep all five as *analytic* categories but to report an inter-frame confusion matrix and treat the two overlapping pairs as a robustness concern, not to assume clean orthogonality.

## C. Table of Historical Anchor Variants (Frame × Epoch × Language)

Anchors are epoch-specific; cells marked **[N/E]** denote concepts not lexically existent in that epoch. This table is illustrative of the equivalence-mapping principle, not exhaustive.

| Frame | UK→DE 1870–1914 (EN) | USA→JP 1965–95 (EN) | EC/EU→JP 1965–95 (EN/FR/DE) | US/DE/FR→CN 1995– (EN/DE/FR) |
|---|---|---|---|---|
| **Security / strategic threat** | "German menace", "naval race", "gigantic commercial State … to menace our prosperity" (Williams 1896) | "economic Pearl Harbor", "Japan as conqueror" | "Fortress Europe" defensive framing; MITI as state actor | "China threat", "systemic rival"/"Systemrivale", "de-risking", "economic security" |
| **Unfair competition / rule-breaking** | "unfair foreign competition", "pauper labour", "sweated goods", "bounties"/"subsidised transport" (Williams 1896; Tariff Reform League 1903) | "dumping", "closed markets", "non-tariff barriers", "level playing field" | "dumping", VER, "screwdriver plants", "voluntary export restraint" | "dumping", "state subsidies", "overcapacity", "non-market economy", "level playing field" |
| **Systemic-ideological conflict** | **[largely N/E]** — rivalry framed as liberal-imperial, not ideological | "Japan Inc.", "the Japan Model", MITI planning vs. free markets | "Japan Inc.", model competition; state-directed capitalism | "state capitalism", "authoritarian model", "Systemrivalität", CCP-directed economy |
| **Deindustrialization / employment threat** | "industrial supremacy … departing", displacement of British goods (Williams 1896) | "sweep up around Japanese computers" (Mondale), "hollowing out", Rust Belt | job losses, plant closures, "désindustrialisation" | "China Shock" (Autor, Dorn & Hanson 2016), "Second China Shock", job losses |
| **Technology appropriation / espionage** | "German spies", "Spies of the Kaiser" (Le Queux 1909); reverse-engineering of British goods; **"forced technology transfer" [N/E]** | "they get all our science papers", copying/imitation, process-technology transfer | technology-transfer-for-market-access; **[FTT term N/E]** | "forced technology transfer", "IP theft", "cyber espionage", "industrial espionage" |

Key drift markers: **"forced technology transfer"** is a post-2017 lexicalization (crystallized by the USTR Section 301 findings of 22 March 2018) with no pre-existing single-term equivalent; the earlier equivalents are diffuse ("copying", "imitation", "reverse engineering", "espionage"). **"Social dumping"** and **"level playing field"** are late-20th-century coinages whose 1900s equivalents are "pauper labour"/"sweated goods". **"Systemic rival"** in the China context dates to the European Commission/HRVP joint communication "EU-China – A Strategic Outlook" of 12 March 2019 (JOIN(2019) 5 final), which describes China as, "simultaneously, in different policy areas, a cooperation partner with whom the EU has closely aligned objectives, a negotiating partner with whom the EU needs to find a balance of interests, an economic competitor in the pursuit of technological leadership, and a systemic rival promoting alternative models of governance." *(Verified verbatim against the Joint Communication.)* The espionage anchor is trans-epochal in surface form ("spy") but shifts referent from military/naval reconnaissance (Edwardian) to commercial/IP theft (China era) — a case of stable form with drifting sense that must be disambiguated by context in the classifier.

## D. Archive Landscape Map by Dyad

**UK→Germany (1870–1914):**
- *The Times Digital Archive* (Gale/Cengage): coverage 1785–2019/2013 (varies by provider vintage); the initial run 1785–1985 was digitized in a consistent 2002–2003 campaign (first batch 1936–1946, growing to 1880–1985 by end-2002, whole run by close of 2003); over 1.6 million pages / 70,000 issues / zoned into 11.8 million articles; issue-level XML; commercial license/paywall; text-mining access via Gale Digital Scholar Lab / drives; consistent OCR from a single digitization campaign. *(Figures verified against the Oceanic Exchanges data report and digitisednewspapers.net.)* This is the strongest single primary source for the earliest dyad.
- *British Library 19th Century Newspapers*, *Daily Mail Historical Archive (1896–2004)*, *Economist Historical Archive*, *Financial Times Historical Archive* (all Gale) provide political-orientation spread.
- Caveat: over-reliance on The Times is a known distortion in Victorian scholarship (Hobbs 2013, "the deleterious dominance of The Times in nineteenth-century scholarship").

**USA→Japan and USA→China:**
- *ProQuest Historical Newspapers* (TDM collection): approximately 99.1 million XML full-text files across 26 titles (incl. New York Times back to 1851); per-article OCR quality scored against a word corpus; access via ProQuest TDM Studio or institutional HPC; commercial license; not being updated. *(Verified against the NYU TDM guide.)* Strong for USA→Japan (1965–95) and USA→China (1995–).
- *Chronicling America* (Library of Congress / NDNP): freely accessible, public-domain newspaper pages through 1963; loc.gov JSON API (the site is migrating; a legacy dedicated API and OCR page endpoints are being retired/redirected in 2025–2026 [genaue Migrations-/Redirect-Daten: nicht prüfbar in dieser Runde]); bulk OCR datasets; open license. Excellent for pre-1963 US material but ends before the Japan and China peaks.

**EC/EU→Japan (1965/70–1995):**
- *Institutional*: EUR-Lex hosts the Official Journal (including the Annex "Debates of the European Parliament") from 1952 to present; comprehensive OJ digitization completed 2008; machine-readable access via the Cellar repository (SPARQL endpoint + RESTful API), bulk data, Formex/XML/PDF/HTML; CELEX and ELI persistent identifiers; all official languages (fewer for pre-enlargement documents). MultiEURLEX and JRC-Acquis are derived research corpora.
- *European Parliament verbatim debates*: published as the OJ Annex (Compte Rendu in Extenso); print publication ceased in 1999. **Critical access split**: the EP plenary portal's searchable database of proceedings reaches back only to ~1994; **pre-1994 debates are available only as OJ-Annex scans via EUR-Lex/Publications Office (OJ from 1952) and via the EP Historical Archives**. Word-level full-text search of the earliest debates is therefore limited. *(EP "post-1994 searchable / pre-1994 Annex-only" split verified against the Globalex and Georgetown Law EU guides.)* LinkedEP (van Aggelen et al. 2017, *Semantic Web Journal*) provides RDF/SPARQL Linked Open Data of verbatim reports; the Europarl Corpus is the MT-derived derivative.
- *Member-state press (aggregated)*: French coverage strong via Gallica/RetroNews (below); German via ZEFYS but with a hard stop c. 1950 (below), making the EU "aggregate" index only partially disaggregable by member state.

**France (FR→Japan/China):**
- *Gallica* (BnF): free, open access, millions of documents; newspapers/periodicals 19th–20th c.; IIIF access; open for public-domain material.
- *RetroNews* (BnF-Partenariats): ~600 (growing) digitized French titles, coverage effectively 1631–1950; full-text search, term-frequency tools, bulk download for subscribers; OCR + semantic enrichment; subscription/paywall for advanced features. *(600-title/French-press scope verified against BnF and BSB; the "~15 million articles" figure: nicht prüfbar in dieser Runde.)* Coverage effectively ends c. 1950, so the FR→China (post-1995) window is NOT covered by RetroNews and must rely on commercial contemporary archives (Le Monde, Le Figaro, AFP) — a coverage gap for the modern French dyad.

**Germany (DE→China; and UK→DE target-side context):**
- *Deutsches Zeitungsportal* (Deutsche Digitale Bibliothek): digitized historical German newspapers c. 1671–1950; full-text search; sub-portal of DDB.
- *ZEFYS* (Staatsbibliothek zu Berlin): roughly 190–220 titles, focus ~1857–1939 (some catalogues extend later, incl. DDR-Presse); IIIF access with ZDB-ID + date persistent-URL scheme; ALTO/METS XML; APIs only for public-domain titles; OCR coverage is partial and OCR text is not used for full-text search in the main ZEFYS interface; Fraktur font degrades OCR. *(Titles/date-focus and "OCR not used for full-text search" sourced to the Stabi Lab / digitisednewspapers pages; the specific "~50% OCR / ~311,234 issues" figures: nicht prüfbar in dieser Runde.)*
- *Impresso* (Media Monitoring of the Past; Swiss/Luxembourgish core, expanding to Western Europe incl. Germany): multilingual historical newspaper corpus with REST API + Python library (Impresso Datalab), semantic enrichments, OCR-quality assessment, OCR-robust multilingual embedding models; access managed per copyright.
- **Structural gap**: the German China-debate (post-1990) lives in *Der Spiegel* archive, *Die Zeit* archive, the *FAZ* archive, *Frankfurter Rundschau*, and *Handelsblatt* — all commercial, license-gated, without bulk full-text/API access. This is the single largest archival obstacle to the DE→China dyad.

**Australia (comparative/context):** *Trove* (National Library of Australia) — a large open digitized newspaper corpus with an API — is available as an English-language robustness check but is peripheral to the four core dyads.

## E. Chronology of Known Tension Peaks by Dyad (for later validation)

**UK→Germany:**
- 1887: Merchandise Marks Act (50 & 51 Vict. c. 28, royal assent 23 August 1887) requires country-of-origin marking of imported goods, producing the "Made in Germany" label. *(Verified.)*
- 1896: E. E. Williams, *Made in Germany*, first serialized in the New Review in five installments in early 1896, then republished as a book that ran through six editions before the year was out; "a gigantic commercial State is arising to menace our prosperity"; contemporaneous with the Kruger telegram. *(Verified verbatim.)*
- 1903–1906: Joseph Chamberlain's Tariff Reform campaign (Tariff Reform League founded 1903); "unfair foreign competition", "pauper labour" discourse peaks.
- 1906–1909: Invasion/spy-fever literature (Le Queux, *The Invasion of 1910* 1906; *Spies of the Kaiser* 1909); 1909 creation of the Secret Service Bureau; Anglo-German naval race.

**USA→Japan:**
- 1977: escalating US-Japan trade tension.
- 1981: Japanese voluntary export restraint on autos.
- 1985: "The Danger From Japan" (New York Times Magazine); Plaza Accord; SIA Section 301 semiconductor petition (June 1985).
- 1986: US–Japan Semiconductor Agreement (signed 2 September 1986). Japan's global mass-manufactured-semiconductor share rose from 28% to 50% between 1978 and 1987 (US share fell 55%→44%); US DRAM share fell from 70% to 20% between 1978 and 1986 as Japan's rose from under 30% to ~75%. *(Verified against the NBER/Irwin study and the 1986 agreement record.)*
- 1987–1989: "Japan Inc." panic peak; Japanese FDI/real-estate acquisitions; Mondale's "sweep up around Japanese computers"; large US-Japan bilateral deficit toward the end of the decade [genauer 1989-Betrag von ~49 Mrd. USD: nicht prüfbar in dieser Runde].
- Post-1990: Japanese asset-bubble collapse deflates the panic.

**EC/EU→Japan:**
- 1979: leaked confidential internal memo by Sir Roy Denman, then Director-General for External Affairs of the EC Commission (1977–82), describing the Japanese as "workaholics living in rabbit hutches". *(Quote and 1979 leak verified against multiple records incl. Hansard 1989 and JIIA; the specific secondary attributions used in the draft could not be confirmed to contain the quote and have been dropped.)*
- 1982: Poitiers incident — France routes all Japanese VCR imports through the small inland Poitiers customs post (staffed by ~two agents) to throttle imports (CBC, 19 Nov 1982); Commission Regulation (EEC) No 3545/82 of 21 December 1982 introduces Community surveillance of Japanese video-tape-recorder imports (Japanese VTR share equivalent to 80.5% of the Community market in H1 1982, per the regulation's recital). *(Verified.)*
- 1983: EC–Japan VER on video cassette recorders (MITI–EC).
- 1987: EC's first anti-circumvention ("screwdriver plant") regulation, Council Regulation (EEC) No 1761/87 of 22 June 1987 amending Reg. (EEC) No 2176/84 (OJ L 167, 26.6.1987); the "screwdriver" provisions were later found GATT-inconsistent (1990 panel). *(Regulation citation verified against EUR-Lex.)*
- 1991: EC–Japan car agreement ("Elements of Consensus", Brussels, 31 July 1991; operative 1993–1999).

**USA/Germany/France→China:**
- 2001: China's WTO accession.
- May 2015: "Made in China 2025" issued by the State Council on 19 May 2015 (notice dated 8 May 2015), under Premier Li Keqiang; the think tank MERICS described it at the time as a "declaration of war on Germany". *(Issuance date and the MERICS characterization verified; the draft's "signed 19 May 2015 by Li Keqiang" wording corrected to State-Council issuance.)*
- 2016: German reversal on the Aixtron takeover (US intelligence warning); Fujian/Grand Chip deal blocked; German unease over Chinese acquisitions (Kuka).
- 2017–2018: USTR Section 301 investigation initiated 18 August 2017 (82 FR 40213) and findings issued 22 March 2018; "forced technology transfer" enters mainstream discourse; White House OTMP report (June 2018). *(Verified.)*
- 12 March 2019: EU "Strategic Outlook" (JOIN(2019) 5 final) labels China "partner, competitor and systemic rival". *(Verified.)*
- 2023–2024: EU "de-risking"; German China strategy; German domestic-intelligence warnings on Chinese industrial espionage (2024); "Second China Shock" discourse.

## F. Measurement Specification

**Layer 1 — anchor-based frequency.** For each frame f, epoch e, and language l, a curated anchor lexicon (seeded from Sections C and E, expanded via word-embedding neighbors within the corpus — with the caveat that embedding neighbors surface OCR errors) yields a count normalized per 100,000 words of the incumbent-country-year corpus. Per-100k-word normalization is the cross-corpus comparability anchor; it does not solve OCR-density differences.

**Layer 2 — supervised classifier.** A multilingual transformer (e.g., an OCR-robust multilingual embedding model of the Impresso type, or XLM-R/mBERT fine-tuned) is trained on a stratified, manually labeled sample (stratified by dyad, epoch, language, and source political orientation), with double-coding and reported inter-coder reliability (target κ > 0.6). The model stores, for every article, a probability for each of the five frames. Manual coding of a 50–100-article validation subset per stratum is the minimum for reliable extrapolation.

**Indices.**
- *FrameIntensity(f, incumbent, target, year)* = mean predicted probability of frame f over target-related articles.
- *SalienceIndex(incumbent, target, year)* = (# target-related economic articles) / (# all economic articles of the incumbent-country-year) — an exposure-normalized measure of attention.
- *OverallIndex* = mean of FrameIntensity across the five frames (optionally salience-weighted).

**Problematic indicators and controls.**
- *Volume-vs-tone confounding*: separate SalienceIndex (volume/attention) from FrameIntensity (tone/schema); never collapse them into one number without reporting both.
- *Base-rate / exposure normalization*: the denominator must be the incumbent-country-year economic-article base, not total articles, to avoid confounding with overall newspaper growth.
- *Classifier drift over time*: train and validate per epoch; report cross-epoch transfer degradation; consider epoch-specific model heads.
- *Language non-equivalence of anchors*: anchors are mapped, not translated literally; validate equivalence with bilingual coders.
- *OCR-induced measurement error*: weight or filter by per-article OCR quality score (available in ProQuest TDM, Impresso); Fraktur-set German pre-1945 material is especially error-prone.
- *Digitization selection bias*: the panel of titles digitized is not a random sample of the press; fix the source panel ex ante where possible and flag where it cannot be (Germany post-1950, France post-1950).

## G. Causality: Measurement versus Interpretation

Measured rhetoric intensity is a valid *indicator* of real economic-political tension only under specific conditions, and is frequently driven by confounds. Rhetoric peaks co-move with material events (the 1986 Semiconductor Agreement, the 2018 Section 301 tariffs, the 1982 Poitiers VCR blockade) — corroborating that rhetoric can track tension. But the same sources show rhetoric is often **event-driven and media-cyclical** rather than tracking underlying fundamentals: during the 1985 US semiconductor downturn, import penetration actually fell (Japan's share of US semiconductor consumption rose from 7.5% in 1982 to 12.3% in 1984 before dropping back to 9.8% in 1986, per Irwin/NBER) even as "dumping" rhetoric peaked [the precise share of the downturn attributable to falling demand vs. imports: Richtung bestätigt, genaue Quantifizierung nicht prüfbar]; the Japan panic collapsed with the asset bubble (1990) rather than with any resolution of the underlying "unfair practices". Alternative drivers of rhetoric spikes to be controlled or acknowledged: **electoral cycles**, **singular scandals/incidents** (Aixtron 2016; specific espionage arrests), and **news-agenda dynamics** (a bestseller like *Made in Germany* 1896 or *Spies of the Kaiser* 1909 manufacturing a discourse wave). The instrument should therefore be presented as measuring *discursive salience and framing*, with tension-tracking treated as a hypothesis to be tested against an independent event chronology (Section E), not assumed.

## H. Heterogeneity: For Whom Comparability Holds

- *By digitization epoch*: comparability is strongest 1965–1995 and 1995–present (born-digital or high-quality OCR) and weakest 1870–1914 (Fraktur German, variable OCR).
- *By dyad*: **robust/confirmatory** — UK→DE (Times Digital Archive), USA→JP and USA→CN (ProQuest); **exploratory only** — DE→CN (post-1990 commercial paywalls), FR→CN (RetroNews ends c. 1950), EC/EU→JP institutional pre-1994 (Annex-only, limited word search).
- *By institutional vs. press level*: EU institutional texts (EUR-Lex, post-1994 EP debates) are machine-readable and reconstructible; the EU press aggregate is only partially disaggregable by member state because German and French modern press are paywalled.
- *By source political orientation*: comparability requires holding orientation constant; the UK dyad has good orientation spread (Times, Daily Mail, Economist, FT), the German modern dyad poor spread under open access.

## Evidence-Strength Assessment by Core Finding

- **Frames map onto the Policy Frames Codebook but are non-orthogonal (security/technology overlap; systemic frame absent for UK→DE): STRONG.**
- **Anchor-based supervised hybrid is the correct operationalization: STRONG** (converges with the computational-framing methodological literature).
- **Semantic drift requires epoch-specific anchor lexica; "forced technology transfer" and "systemic rival" are non-existent before their epoch: STRONG.**
- **Times Digital Archive, ProQuest HNP, Gallica/RetroNews, Chronicling America, EUR-Lex offer programmatic, persistent-ID access: STRONG** (coverage dates and access modes documented from provider/library sources; TDA and ProQuest figures verified this round).
- **The German post-1990 and French post-1950 press dyads lack open bulk/API full-text archives, breaking panel continuity: STRONG.**
- **EP verbatim debates are searchable only from ~1994; pre-1994 is Annex-only: STRONG** (verified).
- **Rhetoric peaks are often event/electoral/media-cycle driven rather than fundamentals-tracking: MEDIUM-STRONG** (illustrative cases strong; systematic causal claim untested).
- **The five frames are historically continuous in surface realization across all dyads: MEDIUM** (continuity clear for four frames; systemic-ideological frame discontinuous).
- **A single seamless cross-epoch comparable index is achievable: WEAK/SPECULATIVE** — tiered, uncertainty-flagged comparability is the realistic ceiling.

## Recommendations

1. **Build the instrument tiered, not uniform.** Ship UK→DE, USA→JP, USA→CN as confirmatory tiers; label DE→CN, FR→CN, and pre-1994 EC→JP as exploratory. Threshold to promote a dyad from exploratory to confirmatory: a fixed, ex-ante source panel with high per-page OCR word-accuracy and programmatic full-text access.
2. **Fix the source panel ex ante per dyad-epoch** and publish it; where a continuous open panel is impossible (Germany post-1950, France post-1950), either license the commercial archive or restrict claims to the open sub-panel and flag it.
3. **Adopt epoch-specific anchor lexica with an explicit equivalence-mapping table** (Section C generalized), version-controlled and released as a reproducibility artifact.
4. **Report SalienceIndex and FrameIntensity separately**; never publish OverallIndex without its components.
5. **Validate against the independent event chronology** (Section E) before making any tension-tracking claim; pre-register the peaks.
6. **Store all intermediate artifacts** (seed lexica, labeled sample, per-article probabilities, OCR-quality scores) to guarantee full reconstructibility.
7. **Treat the systemic-ideological and technology-appropriation frames as robustness-sensitive**; report inter-frame confusion and consider merging where they collapse.

## Caveats

The China-era and Japan-panic comparisons are heavily mediated by present-day commentary that explicitly draws the analogy; these are useful for the event chronology but are secondary sources and carry an analogizing bias that should not be imported into the measurement. Several access details (exact ProQuest title-year lists, ZEFYS OCR coverage percentage, RetroNews article counts, Chronicling America migration/redirect dates) vary across library guides and provider pages and remain flagged [nicht prüfbar] pending direct provider confirmation. The exact terms of the 1983 EC–Japan VCR VER are not crisply documented in open sources.

## References

Autor, D. H., Dorn, D. & Hanson, G. H. (2016) 'The China Shock: Learning from Labor-Market Adjustment to Large Changes in Trade', *Annual Review of Economics* 8, pp. 205–240.
Boydstun, A. E. & Gross, J. H. (2014) *Policy Frames Codebook*.
Card, D., Boydstun, A. E., Gross, J. H., Resnik, P. & Smith, N. A. (2015) 'The Media Frames Corpus: Annotations of Frames Across Issues', *ACL-IJCNLP*, pp. 438–444.
Entman, R. M. (1993) 'Framing: Toward Clarification of a Fractured Paradigm', *Journal of Communication* 43(4), pp. 51–58.
European Commission / HRVP (2019) *EU-China – A Strategic Outlook*, JOIN(2019) 5 final, 12 March 2019.
Gamson, W. A. & Modigliani, A. (1989) 'Media Discourse and Public Opinion on Nuclear Power', *American Journal of Sociology* 95(1).
Gitlin, T. (1980) *The Whole World Is Watching*.
Hobbs, A. (2013) 'The Deleterious Dominance of The Times in Nineteenth-Century Scholarship', *Journal of Victorian Culture* 18(4), pp. 472–497.
Irwin, D. A. (1996) 'Trade Politics and the Semiconductor Industry', in A. O. Krueger (ed.) *The Political Economy of American Trade Policy*, University of Chicago Press, pp. 11–66 (NBER Working Paper 4745, 1994).
Le Queux, W. (1909) *Spies of the Kaiser*.
US Trade Representative (2018) *Findings of the Investigation into China's Acts, Policies, and Practices Related to Technology Transfer, Intellectual Property, and Innovation under Section 301 of the Trade Act of 1974*, 22 March 2018.
van Aggelen, A. et al. (2017) 'The debates of the European Parliament as Linked Open Data', *Semantic Web Journal*.
Williams, E. E. (1896) *Made in Germany*. London: William Heinemann.
Provider/library documentation: Gale / Oceanic Exchanges (Times Digital Archive), ProQuest/NYU (Historical Newspapers TDM), Library of Congress (Chronicling America), BnF/BSB (Gallica/RetroNews), Staatsbibliothek zu Berlin / Stabi Lab (ZEFYS), Deutsche Digitale Bibliothek (Deutsches Zeitungsportal), Impresso Project, EUR-Lex/Publications Office, European Parliament / Globalex / Georgetown Law EU guides.

*[Zuschreibung nicht verifiziert / removed from the citation basis this round: Garon (2011), Asia-Pacific Journal: Japan Focus; Woronoff (1996), Japan as –anything but– Number One — used in the draft for the Denman quote, which is independently and robustly documented elsewhere.]*
