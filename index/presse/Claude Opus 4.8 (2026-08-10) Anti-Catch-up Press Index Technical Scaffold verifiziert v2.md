# A Reconstructable Technical Scaffold for the Dyadic Anti-Catch-up Press Index

*Call 2 of 2 — Synthesis and Technical Delivery. Verified version v2 (2026-08-10); round-1 corrections held, and the two residual [nicht prüfbar] items from round 1 (Bernaciak 2012; "dumping" first-use dating) were confirmed against primary sources this round and their flags discharged. Audience: economist with computational text-analysis skills. All artefacts in English; Harvard-style citation in the documentation.*

## TL;DR
- The index is fully reconstructable if built as a strict three-layer pipeline (article → source-year → country-year) in which every country-year figure deterministically re-derives from a stored article panel; the ten artefacts below (source_registry, frame_dictionary, keyword_filter, labeled_articles, press_articles_panel, press_discourse_index, aggregation logic, non-executed templates, validation_report, documentation) satisfy hypotheses H1–H3, with each reconstructability breakpoint explicitly flagged rather than hidden.
- Confirmatory dyads (UK→DE via the Times Digital Archive; US→JP and US→CN via ProQuest Historical Newspapers TDM; FR→* via Gallica/RetroNews; US context via Chronicling America open bulk OCR) can be executed with real bulk/API access; exploratory dyads (DE→CN, FR→CN, EU/EC→JP pre-1994) cannot, and this asymmetry is hard-coded into the `access_method` and `archive_discontinuity` fields.
- The scaffold is a runnable, seeded template — **not** a collected corpus and **not** a trained model; it prioritises stored intermediate outputs over ephemeral API calls, epoch-specific mapped anchor lexica over a fixed dictionary, and explicit flags over silent omission.

## Key Findings

1. **Three-layer determinism is achievable but has exactly three fragile joints.** (i) The article→country-year aggregation is deterministic *only if* the salience denominator (total economic articles per incumbent-year) is itself a stored, versioned table rather than recomputed on the fly; (ii) the EU up/down aggregation preserves member-country IDs so disaggregation is lossless *only if* the country-year table is never overwritten by the EU composite (append, never overwrite); (iii) classifier outputs must be serialised per-article as probabilities (not just labels), or the OverallIndex cannot be recomputed. Each is addressed below with an explicit stored-output rule.

2. **Anchor terms are epoch-specific and must be mapped, not fixed.** Confirmed from primary sources: **"forced technology transfer"** is a 2017–2018 USTR coinage — the Section 301 investigation into China's technology-transfer, IP and innovation practices was initiated 18 August 2017 (Federal Register 82 FR 40213), with the President's implementing Memorandum and USTR findings released 22 March 2018 (USTR, 2018). **"Systemic rival"** enters EU discourse with the European Commission/HR-VP joint communication *EU–China: A Strategic Outlook* (JOIN(2019) 5 final, 12 March 2019), which defines China as "simultaneously … a cooperation partner … a negotiating partner … an economic competitor in the pursuit of technological leadership, and a systemic rival promoting alternative models of governance." **"Social dumping"** became a widespread public-discourse term chiefly around EU enlargement (Bernaciak, 2012, ETUI Working Paper 2012.06, verified — whose survey spans NAFTA, the EU southern enlargement, and the 2004 eastern enlargement). For the UK→DE 1870–1914 dyad, the period-equivalent anchors are **"unfair competition"** (a legal concept — French *concurrence déloyale* case law from the mid-19th century — entering the Paris Convention only via Article 10bis at the Brussels revision of 14 December 1900, *not* the original 1883 text; verified); the fair-trade critique of Britain's **"one-sided free trade"** (advanced by the Fair Trade League, founded August 1881; verified — note: the League's own newspaper motto was "The Plough, the Shuttle, the Forge, the Ship", so "one-sided free trade" is the movement's argument, not a formal League slogan); **"dumping"** (loose trade sense in English-language trade literature around the turn of the century, theorised as "price discrimination between national markets" by Viner, 1923; verified); and the **"Made in Germany"** stigma created by the Merchandise Marks Act 1887 and dramatised by E. E. Williams's *Made in Germany* (1896). These mappings populate the `historical_variants` column.

3. **The archive landscape dictates which dyads are confirmatory.** The Times Digital Archive delivers "over 1.6 million pages from 70,000 issues, sub-divided or zoned into 11.8 million articles" (Oceanic Exchanges TDA data report), one XML file per article/textual unit with word-level spatial coordinates; the core consistent OCR project covered 1785–1985 (produced 2002–2003) with post-1985 content added on a separate rolling substructure, and the full digitised run now spans 1785–2019 (Gale product). ProQuest Historical Newspapers TDM "consists of approximately 99.1 million XML files … for 26 newspaper titles," with OCR quality scored on a per-article basis and a licence note that "researchers cannot use this data with any products or platforms (including large language models) that may retain" the data (NYU Libraries TDM guide). Chronicling America offers genuinely open bulk OCR (public-domain, batch/OCR downloads with SHA-256 checksums, loc.gov API from 4 August 2025, searchable pages 1756–1963; bulk-OCR rate limit 10 requests / 10 minutes per IP). Gallica/RetroNews covers ~600 core titles (1631–1950) effectively ending c. 1950. German post-1990 press (Der Spiegel, Die Zeit, FAZ, Handelsblatt) has **no** bulk/API full-text and sits behind hard paywalls — the binding constraint on the DE→CN dyad.

4. **Normalisation can conflate volume with tone.** Frame *intensity* (mean predicted probability) and *salience* (share of economic coverage) are deliberately kept as separate columns, and a per-100k-word anchor-rate normalisation is provided, precisely so that a reviewer can test whether an apparent "peak" is a tone shift or merely a volume shift.

## Details

### Artefact 1 — `source_registry.csv`
Ex-ante fixed source panel. Columns: `source_id, source_name, country, political_orientation, start_year, end_year, archive_location, access_method, persistent_id_scheme, archive_discontinuity, dyad_role`.

```csv
source_id,source_name,country,political_orientation,start_year,end_year,archive_location,access_method,persistent_id_scheme,archive_discontinuity,dyad_role
SRC001,The Times (London),GB,centre-right/establishment,1785,2019,Times Digital Archive (Gale),institutional_subscription_XML,Gale_TDA_articleID,"OCR project break 1785-1985 (produced 2002-03) vs rolling post-1985 substructure",confirmatory_UK_DE
SRC002,The Manchester Guardian,GB,liberal-left,1821,2003,ProQuest Historical Newspapers,institutional_subscription_TDM,ProQuest_GOID,"~12yr moving wall on recent issues",confirmatory_UK_DE
SRC003,The New York Times,US,centre-liberal,1851,2021,ProQuest Historical Newspapers TDM,institutional_subscription_XML,ProQuest_GOID,"12-week embargo on recent issues; LLM-reuse forbidden",confirmatory_US_JP_CN
SRC004,The Wall Street Journal,US,centre-right/business,1889,2013,ProQuest Historical Newspapers TDM,institutional_subscription_XML,ProQuest_GOID,"1889-2013 in TDM; recent years separate",confirmatory_US_JP_CN
SRC005,The Washington Post,US,centre-liberal,1877,2008,ProQuest Historical Newspapers TDM,institutional_subscription_XML,ProQuest_GOID,"pre-2008 historical only",confirmatory_US_JP_CN
SRC006,Chicago Tribune,US,centre-right,1849,2015,ProQuest Historical Newspapers TDM,institutional_subscription_XML,ProQuest_GOID,none_known,confirmatory_US_JP_CN
SRC007,Los Angeles Times,US,centre-liberal,1881,2016,ProQuest Historical Newspapers TDM,institutional_subscription_XML,ProQuest_GOID,none_known,confirmatory_US_JP_CN
SRC008,North-China Herald,GB(in China),treaty-port/commercial,1850,1941,ProQuest HN Chinese Collection,institutional_subscription_XML,ProQuest_GOID,"ceases 1941 (Pacific War)",confirmatory_US_CN_context
SRC009,Le Petit Parisien,FR,popular/republican,1876,1944,Gallica/RetroNews (BnF),open_Gallica_IIIF+subscription_RetroNews,Gallica_ARK,"coverage effectively ends ~1944-1950",confirmatory_FR
SRC010,Le Temps,FR,centre/establishment,1861,1942,Gallica/RetroNews (BnF),open_Gallica_IIIF,Gallica_ARK,"ceases 1942; successor Le Monde 1944",confirmatory_FR
SRC011,Le Figaro,FR,conservative,1854,1950,Gallica/RetroNews (BnF),open_Gallica_IIIF+subscription_RetroNews,Gallica_ARK,"RetroNews window ends ~1950",confirmatory_FR
SRC012,Chronicling America pool (US),US,mixed/varies_by_title,1756,1963,Library of Congress NDNP,open_bulk_OCR_API,LoC_lccn+reel,"public-domain; title mix non-random; new loc.gov API from 04-08-2025",confirmatory_US_context
SRC013,Asahi Shimbun,JP,centre-left,1879,2025,Asahi Cross-Search (former Kikuzo II),institutional_paywall_no_bulk,Asahi_articleID,"full-text only from 1984-85; 1879-1989 page scans",exploratory_target_JP
SRC014,Yomiuri Shimbun,JP,centre-right,1874,2025,Yomidas Rekishikan,institutional_paywall_no_bulk,Yomiuri_articleID,"full-text from 1986; images 1874-1989",exploratory_target_JP
SRC015,Der Spiegel,DE,centre-left,1947,2025,Spiegel archive (commercial),hard_paywall_no_API,none_public,"no bulk/API; online from 1994",exploratory_DE_CN
SRC016,Frankfurter Allgemeine Zeitung,DE,centre-right,1949,2025,FAZ-Bibliotheksportal,hard_paywall_no_API,none_public,"no bulk full-text",exploratory_DE_CN
SRC017,Die Zeit,DE,liberal,1946,2025,Zeit archive (commercial),hard_paywall_no_API,none_public,"no bulk full-text",exploratory_DE_CN
SRC018,Handelsblatt,DE,business-liberal,1946,2025,Handelsblatt archive,hard_paywall_no_API,none_public,"no bulk full-text",exploratory_DE_CN
SRC019,European Parliament plenary (verbatim/CRE),EU,institutional,1994,2025,EP Plenary + EUR-Lex OJ Annex,open_API_SPARQL_REST,CELEX_ELI+EP_CRE_id,"searchable verbatim from 1994; pre-1994 only OJ Annex scans via EUR-Lex",exploratory_EU_JP_institutional
```

**H1/H2 check.** Every `source_id` is a stable key reused in the article panel; `dyad_role` marks confirmatory vs exploratory so aggregation code can refuse to compute a confirmatory index from paywalled placeholders. **Reconstructability breakpoint flagged:** SRC013–SRC018 carry `access_method` values that forbid bulk retrieval; any index computed for DE→CN or JP-target dyads is a *template demonstration only*, and the code raises a warning rather than silently emitting a number.

### Artefact 2 — `frame_dictionary.csv`
Five fixed frames; `historical_variants` populated per epoch/language from the Call-1 table and this call's verified sourcing.

```csv
frame_id,frame_name,anchor_terms,historical_variants,inclusion_rules,exclusion_rules
F1,Security/Strategic Threat,"national security; strategic dependence; dual-use; military implications; geopolitical rivalry; supply chain vulnerability","UK-DE 1870-1914: 'commercial menace','trade supremacy','naval/industrial rivalry'; US-JP 1980s: 'economic security','techno-nationalism'; US-CN 2018+: 'systemic rival'(JOIN(2019)5, 12-03-2019),'de-risking','entity list'","article names target country AND a threat-to-nation predicate (security, sovereignty, dependence, strategic sector)","exclude pure military-war reporting with no economic/industrial nexus; exclude sports 'rivalry'"
F2,Unfair Competition/Rule Violation,"dumping; subsidies; state capitalism; currency manipulation; IP infringement; regulatory asymmetry; playing by different rules","UK-DE 1870-1914: 'unfair competition'(concurrence deloyale; Paris Conv. Art.10bis added Brussels 1900),'one-sided free trade'(fair-trade critique; Fair Trade League 1881),'dumping'(loose trade sense c.1900; Viner 1923),'bounty-fed goods','sweated labour'; US-JP 1980s: 'dumping','targeting','closed market','non-tariff barriers'; US-CN 2018+: 'forced technology transfer'(USTR 301, initiated 18-08-2017, findings 22-03-2018),'state subsidies','non-market economy','social dumping'(EU, from 2004/2007 enlargements)","article attributes competitive harm to rule-breaking/asymmetry by target","exclude ordinary price-competition praise; exclude consumer-benefit framings"
F3,Systemic/Ideological Conflict,"authoritarianism; state direction; mercantilism; illiberal economic order; systemic rival; values conflict","UK-DE 1870-1914: 'Prussian state-socialism','protectionist system' (RARE-near-empty per Call 1); US-JP 1980s: 'Japan Inc','developmental state'; US-CN 2018+: 'systemic rival','party-state capitalism','alternative models of governance'(JOIN(2019)5)","article frames conflict as clash of economic-political SYSTEMS/values, not firms","exclude single-firm disputes; exclude tariff mechanics with no systemic claim"
F4,Deindustrialization/Employment Threat,"job losses; factory closures; loss of technological leadership; hollowing out; decline of manufacturing base","UK-DE 1870-1914: 'decay of British industry','loss of trade','workmen thrown idle'; US-JP 1980s: 'Rust Belt','plant closings','hollowing out'; US-CN 2018+: 'China shock','offshoring','manufacturing decline'","article links target competition to domestic employment/industrial-capacity loss","exclude generic recession coverage without target attribution"
F5,Technology Appropriation/Espionage,"technology theft; reverse engineering; forced technology transfer; industrial espionage; IP theft","UK-DE 1870-1914: 'piracy of trade marks','imitation/counterfeit goods','copying English patterns'(Merchandise Marks Act 1887 context; Williams 1896); US-JP 1980s: 'reverse engineering','patent infringement','IBM-Hitachi case 1982'; US-CN 2018+: 'IP theft','cyber-espionage','forced tech transfer'(USTR 301, 2018)","article alleges illegitimate ACQUISITION of technology/designs by target","exclude licensed transfer; exclude legitimate joint ventures framed positively"
```

**Anachronism control.** Because F3 is empirically near-empty for UK→DE (Call 1), the dictionary flags it (`RARE-near-empty per Call 1`) so a reviewer treats a non-zero 1900 F3 score as a probable false positive rather than a finding. Anachronistic anchors ("forced technology transfer," "systemic rival," "social dumping") carry their first-attestation dates so an epoch gate can bar them from earlier strata.

### Artefact 3 — `keyword_filter.json` (+ CSV variant)
Economic/industrial/technological context gate plus exclusion domains, fully documented.

```json
{
  "filter_id": "econ_context_v1",
  "logic": "KEEP if (>=1 include_root within 40 tokens of a target-country mention) AND (0 hard_exclude_root in headline)",
  "include_roots_en": ["trade","tariff","industr","manufactur","export","import","factor","commerc","econom","technolog","patent","subsid","dumping","competition","market","steel","semiconductor","automobile","machinery"],
  "include_roots_de": ["handel","industri","ausfuhr","einfuhr","wettbewerb","zoll","fabrik","wirtschaft","technolog","patent"],
  "include_roots_fr": ["commerce","industri","exportation","importation","concurrence","douan","usine","economi","technologi","brevet"],
  "hard_exclude_domains": ["sport","football","cricket","olympic","art","painting","opera","tourism","travel","recipe","fashion","obituary","weather","racing"],
  "soft_exclude_review": ["war_frontline_only","royal_ceremony","crime_local"],
  "target_country_gazetteer": {
    "DE": ["Germany","German","Prussia","Prussian","Berlin","Reich"],
    "JP": ["Japan","Japanese","Tokyo","Nippon"],
    "CN": ["China","Chinese","Peking","Beijing","Shanghai"]
  },
  "notes": "Roots are stemmed; the 40-token window is stored per hit in the retrieval log for audit. Every exclusion is logged, never silent."
}
```
CSV variant (`keyword_filter.csv`): `filter_id,lang,role,term,window_tokens,notes` with one row per term.

### Artefact 4 — `labeled_articles.csv`
Stratified seed gold set (dyad × benchmark year). Multi-label; `coder` and `notes` retained for inter-coder audit.

```csv
article_id,dyad,benchmark_year,f1_security,f2_unfair,f3_systemic,f4_deindust,f5_techapprop,coder,notes,label_round
LBL0001,UK_DE,1896,0,1,0,1,1,C01,"Made in Germany rhetoric; cheap imitation + jobs",gold_v1
LBL0002,UK_DE,1896,0,1,0,0,1,C02,"trademark piracy angle",gold_v1
LBL0003,UK_DE,1887,0,1,0,1,0,C01,"Merchandise Marks Act debate; unfair competition",gold_v1
LBL0004,UK_DE,1905,1,1,0,0,0,C02,"naval+commercial rivalry blended (F1/F2 overlap)",gold_v1
LBL0005,US_JP,1985,1,1,0,1,1,C03,"semiconductor dumping + Rust Belt + reverse-eng",gold_v1
LBL0006,US_JP,1985,0,1,0,1,0,C04,"Plaza-era closed-market complaint",gold_v1
LBL0007,US_JP,1982,0,0,0,0,1,C03,"IBM-Hitachi espionage case",gold_v1
LBL0008,US_CN,2018,1,1,1,0,1,C05,"Section 301 forced-tech-transfer, systemic",gold_v1
LBL0009,US_CN,2019,0,1,1,0,0,C05,"state-subsidy + systemic-rival framing",gold_v1
LBL0010,US_CN,2001,0,1,0,1,0,C06,"WTO-accession job-loss fears",gold_v1
LBL0011,FR_DE,1896,0,1,0,1,0,C07,"concurrence allemande",gold_v1
LBL0012,UK_DE,1900,0,0,0,0,0,C01,"NEGATIVE: German goods praised, no threat frame",gold_v1
```

Protocol: ≥3 coders per benchmark stratum; disagreements resolved by adjudication; reliability reported as Krippendorff's α (thresholds per Krippendorff, 2013: ≥0.80 reliable, 0.667–0.80 tentative). Published frame-analysis studies commonly report higher reliability for frame *presence* than for frame *classification*, so a second training round precedes gold freeze.

### Artefact 5 — `press_articles_panel.csv`
Article-level panel, seed rows per dyad. Probabilities AND raw anchor counts are stored so the country-year table re-derives without re-running the model.

```csv
article_id,source_id,source_country,incumbent_country,target_country,publication_date,year,language,text_reference_id,target_country_referenced,frame1_prob,frame2_prob,frame3_prob,frame4_prob,frame5_prob,anchor_frame1_freq,anchor_frame2_freq,anchor_frame3_freq,anchor_frame4_freq,anchor_frame5_freq,word_count
ART00001,SRC001,GB,GB,DE,1896-08-21,1896,en,TDA_1896_0821_a17,1,0.12,0.88,0.03,0.71,0.64,0,3,0,2,2,842
ART00002,SRC001,GB,GB,DE,1887-06-14,1887,en,TDA_1887_0614_a09,1,0.09,0.79,0.05,0.55,0.22,0,2,0,1,0,610
ART00003,SRC001,GB,GB,DE,1905-02-03,1905,en,TDA_1905_0203_a04,1,0.74,0.61,0.08,0.20,0.10,2,1,0,0,0,1130
ART00004,SRC003,US,US,JP,1985-09-30,1985,en,PQ_NYT_19850930_a1,1,0.55,0.90,0.12,0.68,0.59,1,4,0,2,1,970
ART00005,SRC004,US,US,JP,1982-06-23,1982,en,PQ_WSJ_19820623_a2,1,0.30,0.20,0.05,0.10,0.86,0,0,0,0,3,540
ART00006,SRC003,US,US,CN,2018-03-23,2018,en,PQ_NYT_20180323_a1,1,0.80,0.85,0.72,0.15,0.66,2,3,2,0,2,1210
ART00007,SRC004,US,US,CN,2019-03-12,2019,en,PQ_WSJ_20190312_a3,1,0.40,0.78,0.70,0.12,0.20,0,2,2,0,0,880
ART00008,SRC009,FR,FR,DE,1896-05-10,1896,fr,ARK_LPP_18960510_a6,1,0.10,0.82,0.02,0.66,0.15,0,2,0,2,0,430
ART00009,SRC001,GB,GB,DE,1900-11-02,1900,en,TDA_1900_1102_a12,0,0.05,0.08,0.01,0.04,0.03,0,0,0,0,0,510
ART00010,SRC019,EU,EU,CN,2019-04-16,2019,en,EP_CRE_20190416_it08,1,0.62,0.70,0.75,0.10,0.30,1,1,2,0,0,1550
```

**Reconstructability breakpoint flagged:** `text_reference_id` points to the stored raw-text object; the panel deliberately does NOT embed full text (licence constraint — Gale and ProQuest TDM terms restrict redistribution and LLM reuse) but must resolve deterministically to the OCR object in the archive. If an archive lacks stable article IDs (e.g. paywalled DE press), `text_reference_id` is set to `NA_no_persistent_id` and those rows are excluded from confirmatory computation.

### Artefact 6 — `press_discourse_index.csv`
Country-year-dyad table with the three EU composites stored in parallel. *(All values below are illustrative placeholders, not measurements.)*

```csv
incumbent_country,target_country,year,frame1_intensity,frame2_intensity,frame3_intensity,frame4_intensity,frame5_intensity,overall_index,salience_index,number_of_articles,total_word_count,eu_index_word_weighted,eu_index_article_weighted,eu_index_equal_weighted
GB,DE,1887,0.09,0.79,0.05,0.55,0.22,0.340,0.021,148,90230,NA,NA,NA
GB,DE,1896,0.11,0.83,0.04,0.66,0.45,0.418,0.058,362,240100,NA,NA,NA
GB,DE,1905,0.71,0.60,0.08,0.22,0.12,0.346,0.049,410,300550,NA,NA,NA
US,JP,1982,0.28,0.35,0.06,0.30,0.70,0.338,0.037,220,150300,NA,NA,NA
US,JP,1985,0.52,0.86,0.11,0.64,0.55,0.536,0.121,905,690400,NA,NA,NA
US,CN,2001,0.30,0.72,0.28,0.61,0.35,0.452,0.088,540,410800,NA,NA,NA
US,CN,2018,0.78,0.83,0.70,0.18,0.63,0.624,0.147,1980,1620500,NA,NA,NA
US,CN,2019,0.60,0.79,0.73,0.14,0.40,0.532,0.131,1750,1440200,NA,NA,NA
FR,CN,2019,0.44,0.60,0.55,0.10,0.22,0.382,0.061,60,88000,NA,NA,NA
DE,CN,2019,0.50,0.66,0.63,0.11,0.28,0.436,0.072,55,84000,NA,NA,NA
EU,CN,2019,0.61,0.71,0.74,0.12,0.31,0.498,0.096,120,181000,0.512,0.498,0.471
FR,DE,1896,0.10,0.82,0.02,0.66,0.15,0.350,0.041,95,52000,NA,NA,NA
```

**H2 check.** The `EU,CN,2019` row carries the EU composites; the underlying member rows (`FR,CN,2019`, `DE,CN,2019`, …) remain in the table with their own `incumbent_country` IDs, so the EU row is fully disaggregable. The composite is appended, never written back over member rows. (Member rows here are template demonstrations, since DE→CN is an exploratory dyad — see registry.)

### Artefact 7 — Aggregation/construction logic (script template)

```r
# 50_aggregate.R  — deterministic; no manual steps; seed fixed upstream at classify stage
library(data.table)
panel      <- fread("press_articles_panel.csv")
econ_denom <- fread("economic_article_counts.csv") # incumbent_country,year,total_economic_articles (STORED, versioned)

# FrameIntensity_f(i,j,t) = mean(pred_prob_f) over relevant (target_country_referenced==1) articles
rel <- panel[target_country_referenced == 1]
fi  <- rel[, .(
  frame1_intensity = mean(frame1_prob), frame2_intensity = mean(frame2_prob),
  frame3_intensity = mean(frame3_prob), frame4_intensity = mean(frame4_prob),
  frame5_intensity = mean(frame5_prob),
  number_of_articles = .N, total_word_count = sum(word_count)),
  by = .(incumbent_country, target_country, year)]

# OverallIndex(i,j,t) = mean_f(FrameIntensity_f)
fi[, overall_index := rowMeans(.SD), .SDcols = paste0("frame", 1:5, "_intensity")]

# SalienceIndex(i,j,t) = target_articles / total_economic_articles(i,t)
fi <- merge(fi, econ_denom, by = c("incumbent_country","year"), all.x = TRUE)
fi[, salience_index := number_of_articles / total_economic_articles]

fwrite(fi, "press_discourse_index_members.csv")   # member/country-year layer preserved
```

```r
# 60_eu_aggregate.R : EU_index(j,t) = weighted mean of member indices; all three weightings stored in parallel
eu_members <- c("FR","DE","IT","NL","ES","PL")     # parametrised, accession-aware member set by year
mem <- fi[incumbent_country %in% eu_members & target_country == "CN"]
eu  <- mem[, .(
  eu_index_word_weighted    = weighted.mean(overall_index, total_word_count),
  eu_index_article_weighted = weighted.mean(overall_index, number_of_articles),
  eu_index_equal_weighted   = mean(overall_index)),
  by = .(target_country, year)]
eu[, incumbent_country := "EU"]
# APPEND (never overwrite) so member rows survive -> H2 lossless disaggregation
```

Weighting is parametrised (`weight_word_count | weight_article_count | weight_equal`); all three columns persist, so the "does the weighting change the ranking?" question is answerable directly from the output.

### Artefact 8 — Parametrised, NON-executed templates
- **Scraping/query template** (`query_templates.yaml`): raw query strings per archive — TDA: `("Germany" OR "German") AND (trade OR industry OR competition OR dumping)` restricted by `daterange`; ProQuest TDM: boolean + `pubdateGTE/LTE`; Chronicling America loc.gov API: `?fa=...&start_date=...&end_date=...&fo=json` (bulk OCR downloads with SHA-256 checksums; rate limit 10 bulk requests / 10 min per IP); EUR-Lex Cellar SPARQL endpoint (`http://publications.europa.eu/webapi/rdf/sparql`) + REST for OJ/EP Annex by CELEX/ELI (timeout + low concurrency, exponential backoff on HTTP 429/503). Retrieval-log schema: `query_id,archive,query_string,run_timestamp,n_hits,n_retrieved,http_status,checksum`.
- **OCR-cleaning regex set** (`ocr_rules.txt`): long-s ſ→s; `rn`→`m` guard; hyphen-linebreak rejoin `(\w+)-\n(\w+)`; whitespace normalisation; digit/letter confusions logged, not auto-applied above a confidence threshold. Every substitution appended to `ocr_change_log.csv` (`article_id,rule_id,from,to,offset`). (Baseline expectation: 19th-century newspaper OCR commonly leaves meaningful character error even after cleaning; see van Strien et al., 2020.)
- **Historical spelling-variant map** (`spelling_variants.csv`): e.g. `shew→show`, `to-day→today`, German `Cölln/Köln`, `Theil→Teil`; per language.
- **Tokenisation/lemmatisation**: language-specific (spaCy/Stanza); config stored.
- **Stopword list** (`stopwords_{en,de,fr}.txt`): standard + archive artefacts (running heads, "ADVERTISEMENT").
- **Classifier training** (`train_classifier.py`): model = domain-adapted BERT-base (continue MLM pre-training on the target-epoch corpus, then supervised fine-tune — the "don't stop pretraining" recipe, Gururangan et al., 2020); example hyperparameters: AdamW, LR 3e-5 (MLM) / 1e-5 (fine-tune), weight decay 1e-4, ε 1e-8, batch 8, 3–6 epochs, max_seq_len 256; stratified 70/15/15 split by dyad×year; metrics precision/recall/F1 + Krippendorff's α vs gold; serialise as `safetensors` + `config.json` + `label_map.json` + `random_seed`.
- **Drift calibration**: retrain every N years (default N = 10, one per epoch regime) with a fixed stability test set carried across regimes; report per-regime F1 delta; flag if the delta exceeds 5 points.
- **Per-100k-word normalisation** (`normalize.R`): `anchor_rate_f = anchor_frame_f_freq / word_count * 1e5`, stored alongside intensity so volume and tone stay separable.

### Artefact 9 — `validation_report.csv`
Known-event flags from the Call-1 peak chronology, matched against index value.

```csv
year,incumbent,target,known_event_flag,event_description,index_value,expected_direction,match
1887,GB,DE,1,"Merchandise Marks Act 1887",0.340,up,partial
1896,GB,DE,1,"E.E.Williams 'Made in Germany'",0.418,up,yes
1905,GB,DE,1,"Anglo-German naval/trade rivalry peak",0.346,up,partial
1982,US,JP,1,"IBM-Hitachi espionage case",0.338,up(F5),yes
1985,US,JP,1,"Plaza Accord; SIA Section 301 + EPROM dumping cases",0.536,up,yes
2001,US,CN,1,"China WTO accession",0.452,up(F4),yes
2018,US,CN,1,"USTR Section 301 findings (22-03-2018); tariffs",0.624,up,yes
2019,US,CN,1,"EU Strategic Outlook 'systemic rival' (12-03-2019)",0.532,up(F3),yes
1900,GB,DE,0,"no salient event (placebo)",0.150,flat,yes
```
The circularity caveat is logged in the documentation `notes`: where an event may itself have driven digitisation/coverage, the peak validation is partially endogenous and is marked `partial`.

### Artefact 10 — Methodological documentation + replication pipeline
Deterministic script order, each writing a stored intermediate:
1. `00_registry_check.R` → validates `source_registry.csv`, refuses confirmatory runs on `hard_paywall_no_API` sources.
2. `10_scrape.py` (parametrised, non-executed) → raw OCR objects + `retrieval_log.csv`.
3. `20_ocr_clean.py` → cleaned text + `ocr_change_log.csv`.
4. `30_filter.py` → applies `keyword_filter.json` → `filtered_articles.parquet` + exclusion log.
5. `40_classify.py` → loads serialised model + seed → writes probabilities to `press_articles_panel.csv`.
6. `50_aggregate.R` → `press_discourse_index_members.csv`.
7. `60_eu_aggregate.R` → appends EU composite rows.
8. `70_validate.R` → `validation_report.csv`.

Determinism guarantees: fixed `random_seed`; pinned package versions (`renv.lock` / `requirements.txt`); SHA-256 content hashes on every intermediate; no interactive edits. Documentation carries Harvard references (e.g. Krippendorff, 2013; Viner, 1923; Williams, 1896; Gururangan et al., 2020; European Commission/HR-VP, 2019).

### Counterarguments (dedicated chapter)
1. **Frame anachronism** — projecting 21st-century categories onto 1900. *Mitigation:* epoch-specific `historical_variants`; F3 flagged near-empty for UK→DE; anachronistic anchors barred from pre-2017 strata by an epoch gate keyed to first-attestation dates. *Not fully solvable:* the act of applying modern categories to 1900 remains interpretive; documented as a standing limitation.
2. **Translation non-equivalence** across languages. *Mitigation:* language-specific include-roots, separate per-language fine-tuning, anchor counts kept language-native. *Partly unsolvable:* "systemic rival" has no clean 1900 equivalent — hence mapping, not translation.
3. **OCR/digitisation selection bias** — which papers survived/were digitised is non-random. *Mitigation:* `archive_discontinuity` flags; per-source salience denominator; Chronicling America title-mix flagged non-random. *Not solvable* by the scaffold — reported as a bias, not corrected.
4. **Classifier drift over 150 years.** *Mitigation:* per-epoch retraining, carried stability set, F1-delta flag.
5. **Comparability illusion (volume vs tone).** *Mitigation:* intensity, salience and per-100k anchor rate stored separately.
6. **Salience-denominator instability.** *Mitigation:* `economic_article_counts.csv` is an explicit, versioned, keyword-defined table, not an on-the-fly count; its definition ships in the replication package and any change bumps a version string.

### What almost nobody asks
- **Is "intensity" interpretable without exposure/base-rate normalisation?** Only weakly; the scaffold therefore refuses to report intensity without the paired salience and per-100k columns.
- **Do the three EU weightings change the ranking?** Answerable because all three are stored; the seed already shows a word- vs equal-weighting spread (0.512 vs 0.471 for EU→CN 2019) — non-trivial, so all three should be reported.
- **Is peak validation circular when events drive digitisation?** Yes in part; flagged `partial` and never used to *tune* the classifier.

### Open research questions (unsolved for a real collection)
- Per-source licence/paywall clearance — German post-1990 press has no bulk full-text, and ProQuest/Gale TDM terms forbid reuse with data-retaining products including LLMs.
- A frozen gold-standard labelling protocol and target inter-coder α across languages/epochs.
- The retraining interval N, and whether a single cross-epoch model is preferable to per-epoch models.
- A defensible, stable definition of "total economic articles" (the salience denominator) across archives with different article-zoning conventions.

## Recommendations
1. **Build and freeze on the fully-confirmatory rails first:** UK→DE on the Times Digital Archive (institutional XML), US→JP/US→CN on ProQuest HN TDM, plus Chronicling America (open bulk OCR) as US context. Freeze the gold set on these before touching exploratory dyads. *Threshold to proceed:* frame-presence α ≥ 0.80 and frame-classification α ≥ 0.667 on the seed gold set.
2. **Treat DE→CN, FR→CN and EU/EC→JP-pre-1994 as explicitly labelled template demonstrations** until access is secured; do **not** publish numeric indices for them. *Threshold to upgrade to confirmatory:* a signed TDM licence or bulk-XML delivery with persistent article IDs. For the EU institutional channel, EP verbatim debates are searchable only from 1994; pre-1994 exists only as OJ-Annex scans via EUR-Lex, so any pre-1994 EU→JP series is scan-dependent, not full-text.
3. **Lock the salience-denominator definition early** and version it; re-running with a changed denominator must bump a version string and trigger a full re-run.
4. **Run the three EU weightings in parallel from day one** and report their rank-correlation; if the Spearman ρ between word- and equal-weighting drops below ~0.9, report all three rather than a single headline EU index.
5. **Retrain per epoch (N ≈ 10 years / one per regime), not once;** promote a single cross-epoch model only if its carried-stability-set F1 is within 5 points of the per-epoch models.

## Caveats
- This is a scaffold with **illustrative** seed data, not a collected corpus or a trained model; all index values shown are placeholders, not empirical measurements.
- Confirmatory/exploratory status is a property of archive access and can change if licences or digitisation windows change; the registry must be re-checked before each run.
- Gale and ProQuest TDM terms in several institutions prohibit use with products that retain data (including some LLM tooling); the pipeline assumes local, non-retentive processing.
- OCR error rates on 19th-century newspapers commonly leave meaningful character error even after cleaning; downstream effects differ by task and are not uniformly negligible.
- The single largest un-fixable threat is digitisation selection bias: the surviving/digitised newspaper set is non-random, so cross-dyad *level* comparisons should be read as within-dyad-over-time signals rather than absolute cross-country magnitudes.
- Historical-etymology datings for "dumping" are now pinned to dictionary evidence: the OED records the noun "dumping" first in 1874 (in Edward H. Knight's mechanical dictionary — a non-trade sense), while the economic sense ("export or throw on the market in large quantities at low prices") is dated by 1868 (Etymonline); the loose protectionist trade usage is turn-of-the-century, and the theory is Viner 1923. Paris-Convention "unfair competition" (Article 10bis) is a 14 December 1900 Brussels addition, not part of the original 1883 text. Both are documented as such in the frame dictionary rather than over-stated.
