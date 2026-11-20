# Policy Amnesia Index - Reference Architecture, v2.5 (forensisch korrigiert, Stand 20.11.2026)

Dyadischer Index zur Messung von Policy Amnesia in Incumbent-Economies - der Grad, in dem Incumbent-Diskurs ueber ein aktuelles Aufholland historisch naheliegende Analogien zur eigenen fruehen Aufhol-, Schutz- oder Industriepolitik auslaesst. Sechs Dyaden, Zeitfenster 1870 bis heute, vollstaendig als CSV reproduzierbar.

## 1. Konzeptioneller Rahmen

### Definition

Policy Amnesia wird operationalisiert als niedrige Rate historischer Selbstreferenz in Dokumenten, die als kompetitiv gegen das Target getaggt sind.

Zwei Sub-Indizes trennen echte Amnesie von thematischer Irrelevanz:

- Sub-Index A (incumbent-centric): Erwaehnungen eigener historischer Episoden relevant fuer Aufholprozesse, Schutz, Industriepolitik, Technologieaneignung.
- Sub-Index B (rival-centric und system-centric): Erwaehnungen historisch vergleichbarer Rival-Episoden (frueherer Targets) oder kanonischer historischer Handelspolitik-Episoden.

Aggregiert zu: AS_total(doc) = 1 - percentile(HRR_total(doc)), mit HRR = (true_history_reference_count / word_count) * 1000.

### Dyaden

- UK -> Deutschland (1870-1914)
- USA -> Japan (1965-1995)
- EG/EU -> Japan (1970-1995)
- USA -> China (ab 1995)
- Deutschland -> China (ab 1995)
- Frankreich -> Japan/China (ab 1970)

## 2. Datenarchitektur

### Drei Ebenen

**Level 1 - Document Segment**:
doc_id, doc_type, source_or_institution_id, incumbent_country, target_country, date, year, language, word_count, competitive_context_flag, history_reference_flag_total, history_reference_count_total, history_reference_count_self, history_reference_count_analogy, history_reference_spans, history_reference_type_codes, uncertainty_flag

**Level 2 - Source-Year Dyadic**:
number_of_docs, total_word_count, share_competitive_context_docs, mean_history_reference_rate_total, mean_history_reference_rate_self, mean_history_reference_rate_analogy, amnesia_score_source_year

**Level 3 - Country-Year Dyadic**:
amnesia_index_total, amnesia_index_self, amnesia_index_analogy, number_of_docs, total_word_count, share_competitive_context_docs, coverage_salience

### EU-Dekomposition

Separate Indizes fuer USA, UK, Deutschland, Frankreich plus EU-Institutionen (EP, Kommission, Rat). Komposit transparent gewichtet in eu_weights_table.csv (Wortzahl- und Dokumentzahl-Gewichte parallel). Gewichtet und ungewichtet.

### CSV-Outputs

Mandatorisch:
1. history_reference_dictionary.csv
2. competitive_context_dictionary.csv
3. documents_registry.csv
4. history_matches_panel.csv
5. labeled_history_spans.csv
6. policy_amnesia_documents_panel.csv
7. policy_amnesia_index.csv
8. eu_weights_table.csv
9. Replikationsskripte plus Klartext-Methodendokumentation

## 3. Historische Referenzklassen

### UK - SELF-Referenzen

**Navigation Acts (1651-1849)**: Kern-Akte 1651 (Rump Parliament, gegen Dutch), 1660, 1663, 1673, 1696. Enumeration abgeschafft 1822 (Wallace-Reformen, nicht Reciprocity of Duties Act), finaler Repeal 1849. Huskisson, Cromwell.
Anker: Navigation Acts, carrying trade, enumerated commodities, English-built ships, repeal.

**Calico Acts (1700, 1721)**: 7 Geo. 1 St. 1 c. 7. Verbot indischer Calico-Importe zum Schutz heimischer Wolle und Seide. Repeal 1774.
Anker: Calico Act, calicoes, Indian cloth, woollen and silk manufactures.

**Technology export bans (bis 1843)**: Verbot Facharbeiter-Emigration (Repeal 1824, Hume), Maschinen-Exportverbot (Repeal 1843, Gladstone als President of Board of Trade).
Anker: emigration of artisans, exportation of machinery, skilled workmen.

**Corn Laws und Repeal (1815-1846)**: Importation Act 1815 (55 Geo. 3 c. 26), Anti-Corn Law League Manchester 1838 (Cobden, Bright). Repeal durch Importation Act 1846 (9 & 10 Vict. c. 22), Commons 327-229 am 15.5.1846, Lords 25.6.1846.
Anker: Corn Laws, corn duties, Anti-Corn Law League, Cobden, Bright, Peel, free trade, cheap bread.

**Workshop of the World (1838-1880er)**: Disraeli-Formulierung Commons 15.3.1838, erneut 15.5.1846 (Corn-Repeal-Debatte, Third Reading, HC Deb 15 May 1846 vol 86 cc616-727). Great Exhibition 1851.
Anker: workshop of the world, industrial supremacy, Great Exhibition.

**Fair Trade movement (1881-1895)**: Fair Trade League Aug 1881, President Earl of Dunraven. Ecroyd Preston by-election Mai 1881. Randolph Churchill Blackpool 24.1.1884 „dead as mutton". Aufgeloest 1895.
Anker: Fair Trade, Fair Trade League, reciprocity, retaliation, Dunraven, Ecroyd.

**Made-in-Germany-Panik (1887-1900er)**: Merchandise Marks Act 1887 (50 & 51 Vict. c. 28), Sheffield Cutlers' Company-Petition Februar 1887 (mit Mundella MP). E. E. Williams, Made in Germany (1896): sechs von acht Kapiteln (Williams-Preface Oktober 1896) bereits in New Review Vol. 14 Nr. 80-85 (Jan-Juni 1896) erschienen, Buchausgabe William Heinemann 1896 (sechs Auflagen bis Jahresende).
Anker: Made in Germany, Merchandise Marks Act, country of origin, German competition, Williams.

**Tariff Reform (1903-1910)**: Chamberlain Birmingham Town Hall 15.5.1903. Ruecktritt September 1903. Glasgow 6.10.1903 (St Andrew's Hall). Tariff Reform League 1903, ca. 250.000 Mitglieder 1914 (Thackeray 2006, History 91). Chamberlain-Schlaganfall 11.7.1906 (History Today/Dutton; Minderheitsvariante 13.7. verworfen). 1906 General Election: Liberals 397, Unionists 156 (Konservative plus Liberal Unionists zusammen).
Anker: tariff reform, imperial preference, Chamberlain, Birmingham, fiscal reform, big loaf.

**Import Duties Act 1932**: 22 & 23 Geo. 5. c. 8. Neville Chamberlain. Commons 454-78. Ottawa Conference 21.7.-20.8.1932.
Anker: Import Duties Act, Ottawa, Empire Free Trade.

### USA - SELF-Referenzen

**Hamilton Report on Manufactures (1791)**: Kongress 5.12.1791. Infant industry protection durch bounties plus moderate Schutzzoelle.
Anker: Report on Manufactures, Hamilton, infant industry, bounties.

**American System (1816-1860er)**: Clay House-Rede 30.-31.3.1824. Tariff 1816, Tariff of Abominations 1828 (ca. 45-50% auf dutiable), Morrill Tariff 1861.
Anker: American System, Clay, protective tariff, Home market, Morrill.

**McKinley und Dingley Tariffs (1890, 1897)**: McKinley 1.10.1890, Anstieg 38%->49,5%. Dingley 24.7.1897, ca. 52%.
Anker: McKinley Tariff, Dingley Tariff, Napoleon of Protection.

**Smoot-Hawley (1930)**: Signiert 17.6.1930. 20.000+ Gueter. Anstieg ca. 40%->~59% auf dutiable (Spezialzoll-Deflations-Artefakt). 1.028 Oekonomen-Petition. US-Importe -66% (4,4 Mrd. $ -> 1,5 Mrd. $, 1929-33).
Anker: Smoot-Hawley, Hawley-Smoot, Tariff Act of 1930, retaliatory tariffs.

**SEMATECH (1987-1997)**: Konsortium gegruendet August 1987, operativ in Austin November 1988. 14 Gruendungsmitglieder. Autorisierung durch NDAA 1988: 100 Mio. $/Jahr ueber fuenf Jahre (500 Mio. $ gesamt). Tatsaechlich dispensiert FY1988-FY1996: ca. 870 Mio. $ (CRS R44544). DoD-interne Schlussbilanz (Final Report 1997): 848 Mio. $ Regierungsinvestition gegen 863 Mio. $ Industrie.
Anker: SEMATECH, DARPA, semiconductor consortium, VHSIC.

**CHIPS Act (2022)**: Signiert 9.8.2022. 52,7 Mrd. $ fuer Halbleiter (39 Mrd. $ Fab + 13 Mrd. $ R&D), 25% ITC. Senate 64-33. US-Weltmarktanteil Halbleiterproduktion 37% (1990) -> 12% (2020) laut SIA/Neuffer.
Anker: CHIPS Act, reshoring, semiconductor subsidies, onshoring.

**COCOM, Toshiba-Kongsberg (1949-1994, 1987-Affaere)**: COCOM 17 Mitglieder. Toshiba-Kongsberg: acht Maschinen in zwei Tranchen - Tranche 1 April 1981 (vier MBP-110 Neun-Achs-Froesen, 17,4 Mio. $, plus Kongsberg NC-2000 Controller), Tranche 2 April 1983 (vier MF-Serie Fuenf-Achs, 10,7 Mio. $). Omnibus Trade Act 1988: 3-Jahres-Importverbot. COCOM aufgeloest Maerz 1994, Wassenaar 1996.
Anker: COCOM, export controls, Toshiba-Kongsberg, dual-use, Wassenaar.

**Section 301 (ab 1974)**: Trade Act 1974 Title III (19 U.S.C. §§2411-2420). Super 301 im Omnibus Trade Act 1988. 130 Faelle 1975-2020, 35 nach WTO (27% der Faelle, Cato/CRS). 2018-Zoelle auf ca. 370 Mrd. $ chinesischer Importe (7,5-25%, ca. 75% der Importe).
Anker: Section 301, Super 301, USTR, unfair trade practices, forced technology transfer.

### Deutschland - SELF-Referenzen

**Friedrich List (1841)**: Das nationale System der politischen Oekonomie, Stuttgart/Tuebingen, J. G. Cotta. USA 1825-1832. Outlines of American Political Economy (1827). Erziehungszoll.
Anker DE: Friedrich List, Erziehungszoll, nationales System, produktive Kraefte, Stufentheorie.

**Zollverein (1818-1871)**: Preussisches Zollgesetz 26.5.1818. Zollvereinigungsvertrag 22.3.1833, in Kraft 1.1.1834. Vorher ca. 1.800 Zollbarrieren im deutschsprachigen Raum. Motz, Delbrueck.
Anker DE: Zollverein, Deutscher Zollverein, Zollvereinigungsvertrag, Preussisches Zollgesetz.

**Bismarcks Schutzzoll (1879)**: Reichstag 12.7.1879 (Britannica-Datum 12.6. falsch). Ehe von Eisen und Roggen. Zolltarifgesetz 15.7.1879. Franckenstein-Klausel 130 Mio. Mark Obergrenze.
Anker DE: Schutzzoll, Schutzzollpolitik, Eisen und Roggen, Zolltarifgesetz, Franckenstein-Klausel.

**Industrieller Aufholprozess (1870-1914)**: Deutsche Bank 1870, Dresdner Bank 1872, Commerzbank 1870. Technische Hochschulen. Reuleaux Philadelphia 1876 „billig und schlecht". Deutsche Gesamtaussenhandel 7 Mrd. Mark (1880) -> 21 Mrd. Mark (1913) (Hungerland/Wolf 2022); Export-Anteil daran grob halb (2,8 -> 10,3 Mrd. Mark, nicht verbatim gegen Hoffmann 1965 verifiziert, konsistent).
Anker DE: Aufholprozess, Universalbanken, Technische Hochschulen, Gruenderzeit, chemische Industrie.

**Wirtschaftswunder (1948-1965)**: Waehrungsreform 20./21.6.1948. Leitsaetzegesetz 18.6.1948. Erhard. Marshall Plan ca. 1,4 Mrd. $ fuer Westdeutschland. Londoner Schuldenabkommen 27.2.1953. Mueller-Armack, soziale Marktwirtschaft.
Anker DE: Wirtschaftswunder, soziale Marktwirtschaft, Waehrungsreform, Wiederaufbau, Londoner Schuldenabkommen.

**Wandel durch Handel / Ostpolitik (1963-2022)**: Bahr Tutzing 15.7.1963. Moskauer Vertrag 12.8.1970. Brandt Kniefall 7.12.1970. Scholz Zeitenwende 27.2.2022.
Anker DE: Wandel durch Handel, Wandel durch Annaeherung, Ostpolitik, Zeitenwende, Annaeherung durch Verflechtung.

### Frankreich und EG/EU - SELF-Referenzen

**Colbertismus (1661-1683)**: Colbert Controller-General 1665-1683. Tariff of 1667 (Verdopplung der Zoelle). Manufactures royales: Gobelins 1662/1667, Beauvais 1664, Manufacture royale de glaces de miroirs 1665. Compagnie des Indes orientales 1664. Canal du Midi 1681.
Anker FR: colbertisme, Colbert, mercantilisme, manufactures royales, protectionnisme, tarif de 1667.

**Commissariat du Plan (1946-2006)**: Dekret 3.1.1946 unter de Gaulle. Monnet erster Commissaire general. Plan Monnet 1947-1953. ERP-Hilfe ca. 20% der franzoesischen Investitionen 1948-52.
Anker FR: Commissariat general du Plan, planification indicative, Plan Monnet, modernisation.

**Dirigisme und Nationalisierungen**: 1. Welle 1944-46 (Renault 16.1.1945, Banque de France Dezember 1945, EDF/GDF 8.4.1946). 2. Welle 1981-82 (Mitterrand-Nationalisierungsgesetz Februar 1982): CGE, Pechiney, Rhone-Poulenc, Saint-Gobain, Thomson, Dassault, Matra, Usinor, Sacilor, Bull plus 36 groesste Banken, Kosten 58 Mrd. Francs (Dissent). Trente Glorieuses durchschnittlich ca. 5% Wachstum (4,6% 1948-63, 5,8% 1960er, Vinen 1996).
Anker FR: dirigisme, champions nationaux, nationalisations, grands projets, Trente Glorieuses, tournant de la rigueur.

**Plan Calcul (1966-1975)**: Interministerieller Rat 19.7.1966. CII Dezember 1966. IRIA Januar 1967. Erste fuenf Jahre > 100 Mio. $ (Wikipedia Plan Calcul, Fosse/Allegre). Servan-Schreiber Le Defi americain Oktober 1967. Unidata-Konsortium 1973-75.
Anker FR: Plan Calcul, defi americain, CII, Servan-Schreiber, souverainete technologique.

**Airbus (1967-)**: Juli 1967 Regierungsankuendigung (NYT 26.7.1967). MoU unterzeichnet 26.9.1967 London (Frankreich/BRD/UK). Airbus Industrie GIE gegruendet 18.12.1970. A300 Erstflug 28.10.1972, Air France Mai 1974. Launch aid kumulativ ca. 22 Mrd. $ bis 2018 (US-Dollar, nicht Euro). Erster operativer Gewinn 1990 (Airbus Corporate History). 2003 Boeing ueberholt (305 vs. 281 Deliveries). WTO DS316 und DS353. Staatsanteile Frankreich ca. 11%, Deutschland ca. 11%, Spanien ca. 4%.
Anker FR/EN: Airbus, aide au lancement, Member State Financing, juste retour, launch aid.

**Poitiers VCR-Blockade (1982-1983)**: Fabius-Dekret 22.10.1982. Poitiers-Zollstelle mit kleiner Besatzung. Vor der Massnahme ca. 50.000 Einheiten/Monat Zollkapazitaet, nach Umleitung ca. 8.000/Monat (einzige Quelle: JAPON-FR; CBC-Alternative 25.000/Woche; Electronics Weekly 53.000 August 1982 -> ca. 1.000 November 1982). Franzoesischer VCR-Markt 1982: ueber 600.000 Einheiten, Verdopplung gegenueber 1981 (260.000 -> 660.000). Ca. 90% Japan-Importanteil (CBC/Bazay). Cresson „Japonais / fourmis jaunes / little yellow men" dokumentiert ab 1991 waehrend ihres Premierats (Newsweek „Hurricane in a Chanel Suit", 26.5.1991). „Rabbit hutches" ist 1979-Denman-Memo (nicht Cresson), Sir Roy Denman als Director-General for External Relations der EG-Kommission.
Anker FR/EN: bataille de Poitiers, magnetoscopes, dedouanement, Cresson, protectionnisme.

**EG/EU Trade Defence von Japan zu China**: EG-Antidumping-Verordnung seit 1968. 2019: 51% aller EU-AD-Zoelle in Kraft (61 von ca. 120 Faellen) gegen China (CEPR/Sandkamp). EU-Japan Elements of Consensus 31.7.1991 (HAEU FL-713, Mason 1994): UK 11% SMMT-JAMA-Deckel (seit 1977 Gentlemen's Agreement; Walker: operatives Band 9-11%), Frankreich 3%, Italien 1,5%. EU Investment Screening Regulation 2019/452, voll anwendbar 11.10.2020. EU-China Market Economy Status: Art. 15 des WTO-Beitrittsprotokolls lief am 11.12.2016 aus.
Anker EN/FR: anti-dumping, Elements of Consensus, Market Economy Status, FDI screening, significant distortions, Fortress Europe.

### ANALOGY-Referenzen

**Plaza Accord (1985)**: 22.9.1985 Plaza Hotel NYC. USD/JPY von ca. 242 auf ca. 120 bis 1988. Louvre Accord 22.2.1987.
Anker: Plaza Accord, Plaza Agreement, G5, Louvre Accord, プラザ合意.

**US-Japan Semiconductor Agreement (1986)**: Unterzeichnet 2.9.1986. Geheime Nebenklausel ~20% Marktanteil-Ziel bis 1991. US-Zolle 300 Mio. $ im April 1987 (Verkuendung 27.3., in Kraft 17.4.1987). Japanischer DRAM-Weltmarktanteil 75% (1987) -> 20% (2001).
Anker: Semiconductor Agreement, STA, 20% market share, 日米半導体協定.

**VER-Episoden**: Japan-Auto-VER USA ab 1.5.1981, 1,68 Mio. Einheiten (1981-83), hoch auf 2,3 Mio. (1985). Multi-Fibre Arrangement 1974-2005.
Anker: VER, voluntary export restraint, Multi-Fibre Arrangement, 輸出自主規制.

**WTO/GATT-Beitritts-Analogien**: Japan GATT-Beitritt 10.9.1955 mit Art. XXXV-Verweigerung durch UK, Frankreich, Australien. China WTO-Beitritt 11.12.2001 (PNTR Oktober 2000). Section 15 NME-Expiry 11.12.2016.
Anker: GATT Article XXXV, PNTR, WTO accession protocol, non-market economy, 入世.

**Currency-Manipulation-Analogien**: Japan Yen (1980er, Lost Decade). China Renminbi (2003-2015). Schumer-Graham Bill S.295 (2005), drohte 27,5% Pauschalzoll.
Anker: currency manipulation, Schumer-Graham, Treasury FX report, 人民币汇率.

**Technology-Transfer-Disputes**: Japan Reverse Engineering (1950-60er, Transistor Bell Labs 1952). Forced Technology Transfer (China, WTO DS542, 2018). Toshiba-Kongsberg (1987).
Anker: technology transfer, forced technology transfer, reverse engineering, 東芝機械ココム違反事件.

**Japan/Korea als China-Analogien**: Japan Inc. (Chalmers Johnson, MITI and the Japanese Miracle, 1982). Keiretsu (系列). Korea Inc., Chaebols (재벌). Discourse-Template von Prestowitz Trading Places (1988, Japan) zu The World Turned Upside Down (China) transferiert.
Anker: Japan Inc, Korea Inc, developmental state, MITI model, chaebol, keiretsu.

**Made-in-Germany -> Made-in-Japan -> Made-in-China**: Alle drei Labels urspruenglich stigmatisierend, dann Qualitaetssignal.
Anker: Made in Germany, Made in Japan, Made in China, late industrializer, 後発工業国.

## 4. Detektionsstrategie

### Layer 1 - Anchor Matching

Deterministisches Matching mit Fuzzy-Toleranzen (Levenshtein, je nach Termlaenge zu spezifizieren; OCR-Risk-Flag). Spans in history_matches_panel.csv mit match_confidence und ocr_risk_flag.

### Layer 2 - Supervised Disambiguation

Fuer ambige Anker (Hamilton, List, Plaza, Clay) stratifiziertes Labelled-Sample in labeled_history_spans.csv. Einfaches, auditierbares Modell (z.B. Logit mit Kontextfenster-Features). Rohe Matches und gefilterte True-Matches beide speichern.

### HRR und Amnesia Score

- HRR_total(doc) = true_history_reference_count_total / (word_count / 1000)
- HRR_self(doc), HRR_analogy(doc) analog
- Jahr-Dyade-Means ueber kompetitiv-getaggte Dokumente

Normalisierung:
- Hauptvariante (Perzentil): AS_total(doc) = 1 - percentile(HRR_total(doc)), innerhalb Incumbent × doc_type × Dekade
- Robustheits-Variante (log-cap): AS_total(doc) = 1 - min(log(1+HRR) / log(1+HRR_cap), 1)

Beide speichern.

## 5. EU-Handhabung

Separate Reihen fuer:
- Nationale Incumbents: USA, UK, Deutschland, Frankreich
- EU-Institutionen: EP, Kommission, Rat (wo Text)

EU-Komposit:
EU_amnesia_total(j,t) = weighted mean of member-state und EU-institution indices

Gewichte explizit in eu_weights_table.csv (Wortzahl- und Dokumentzahl-Gewichte beide). Gewichtet und ungewichtet.

## 6. Validierung

### validation_amnesia_events.csv

Spalten: year, incumbent, target, known_high_salience_episode_flag, expected_direction, observed_amnesia_total/self/analogy.

Validierungs-Episoden pro Dyade:
- UK-DEU: Royal Commission on Depression 1885-86, Merchandise Marks 1887, Williams-Panik 1896, Chamberlains Tariff Reform, Naval Race.
- USA-JPN: Nixon Shock / Textile 1969-71, Auto-VER 1981, Semiconductor Agreement 1986, Omnibus Trade Act 1988, FSX 1989, Japan-Inc-Discourse Peak 1989-93.
- USA-CHN: PNTR 1999-2001, Currency-Debatten 2005-10, MIC2025 ab 2015, Section 301 2017-18, Huawei/Entity List, CHIPS Act 2022, Chip Export Controls Okt 2022/2023.
- DEU-CHN: Kuka-Uebernahme 2016, MIC2025, BDI Partner-Wettbewerber-Papier Januar 2019, Investment Screening Tightenings 2017-24, China-Strategie Juli 2023, VW/Auto-Abhaengigkeit, CAI-Kollaps 2020-21.
- EG-JPN: Elektronik-AD 1977-90er, Poitiers 1982-83, Elements of Consensus 1991, Fortress Europe Semiconductors 1985-92, Screwdriver 1987-90.
- FR-JPN/CHN: Poitiers, Cresson 1991-92, Opposition China MES 2015-16, Decret Montebourg 2014-19, Solar Anti-Dumping 2012-18.

### Kohaerenzcheck

Korrelation mit Indizes 1-3 (Presse, Elite, Policy Action). Amnesie steigt mit Anti-Aufhol-Rhetorik - erwartete Richtung des Thesen-Papers.

## 7. Robustheit

Pflicht:
- All-Target-Mention- vs. competitive-context-only-Dokumente
- Strict vs. expanded Dictionary
- Perzentil- vs. log-cap-Normierung
- Mit/ohne Opinion/Editorials
- Sprachspezifisch vs. englisch-uebersetzt

Alle Robustheits-Outputs in Spalten oder getrennten CSVs, nicht narrativ.

## 8. Multilinguale Pipeline

Original-Sprache primaer, englisch-uebersetzt parallel, Vergleichs-Flags im Dokument-Jahr-Output. Japanische Anker erfordern Unicode plus MeCab-Tokenisierung.

## 9. Offene Spezifikations-Entscheidungen (nicht Faktenlage)

Diese vier Design-Entscheidungen muessen vor Implementierung festgelegt werden:
- Fuzzy-Matching-Schwellenwerte (Levenshtein pro Termlaenge, OCR-Fehlermuster)
- Disambiguierungsregeln fuer ambige Anker (Kontextfenstergroesse)
- EU-Gewichtungsformel (Wortzahl vs. Dokumentzahl; member state vs. institution)
- competitive_context_flag-Schwellenwert (boolesch vs. kontinuierlich, Mindesthaeufigkeit)

## 10. Residual Known-Unknowns (nicht lasttragend)

- Schemla 1993 interne Datierung der Cresson-Japan-Bemerkungen: unextrahierbar; Behauptung einer Times-Aussage 1989 ist unbelegt.
- Monatgenaue Zuordnung der sechs Williams-Kapitel innerhalb New Review Vol. 14 Nr. 80-85: nicht automatisiert lesbar.
- Poitiers 50.000->8.000/Monat: einzig bei JAPON-FR; ~10x-Richtung robust (CBC, Electronics Weekly), konkrete Zahlen variieren.

---

Stand: 20.11.2026, nach sieben Verifikations-Runden stabil. Alle Korrekturen gegen Primaerquellen belegt oder explizit als Einzelquelle/unverifiert markiert.
