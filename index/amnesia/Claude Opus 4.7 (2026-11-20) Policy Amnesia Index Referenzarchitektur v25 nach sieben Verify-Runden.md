# Policy Amnesia Index Referenzarchitektur v2.5 nach sieben Verify-Runden

*Sieben Verifikationsläufe auf eine Deep-Research-Vorlage für einen dyadischen Policy-Amnesia-Index, 1870-heute, über sechs Incumbent-Target-Dyaden.*

## Kernpunkte

1. Die Referenzarchitektur liegt stabil bei v2.5 vor, mit drei verifizierten lasttragenden Zuschreibungen zur Cresson-Japan-Episode (Newsweek-Zitat, Denman als Urheber der „rabbit hutches", kein Primärbeleg für eine Vor-1991-Datierung der „yellow ants") und zwei explizit markierten Einzelquellen (Poitiers-Durchsatz und monatsgenaue New-Review-Hefte).
2. Der Prozess fand und korrigierte ein Dutzend materieller Fehler aus der ersten Fassung, darunter das Wahlergebnis 1906 (397/156 Liberale/Unionisten statt 399/156), der US-Halbleiter-Weltmarktanteil (37 Prozent 1990 statt 40), die Cresson-Attribution (Newsweek 26.5.1991 statt ABC/Chris Wallace) und die Zuordnung der „rabbit hutches" zu Denman 1979 statt Cresson.
3. Das Produkt ist eine ausführbare Deep-Research-Vorgabe mit sechs Dyaden (UK→Deutschland 1870-1914; USA→Japan 1965-1995; EG/EU→Japan 1970-1995; USA→China ab 1995; Deutschland→China ab 1995; Frankreich→Japan/China ab 1970), drei Datenebenen (Document, Source-Year, Country-Year), Zwei-Schichten-Detektion (Anchor Matching plus Supervised Disambiguation) und einem Amnesie-Score AS = 1 − perzentilnormierte Historical Reference Rate HRR.
4. Offen bleiben zwei schwach belegte Einzelangaben (Poitiers-Durchsatz 50.000→8.000 Stück/Monat, einzig bei JAPON-FR; Monat je der sechs Williams-Installments in New Review Vol. 14 Nr. 80-85, Januar-Juni 1896) sowie der innere Datierungsnachweis in Schemla 1993 — alle für die Architektur nicht lasttragend.

## Zweck und Konstrukt

Policy Amnesia misst, wie weit Incumbent-Diskurs über ein aktuelles Aufholland die historisch naheliegenden Analogien zur eigenen früheren Aufhol-, Schutz-, Industriepolitik- oder Rivalitäts-Episode auslässt. Die Architektur operationalisiert das als niedrige historische Selbstreferenz-Rate (HRR) in Dokumenten, die als „kompetitiv" gegen das Target getaggt sind. Zwei komplementäre Sub-Indizes trennen echte Amnesie von thematischer Irrelevanz: Sub-Index A (incumbent-centric) zählt Erwähnungen eigener Episoden, Sub-Index B (rival-/system-centric) Erwähnungen historisch vergleichbarer Rival-Episoden oder kanonischer Handelskonflikte. Der aggregierte Index ist die gewichtete Mischung beider, mit dokumentierter Sensitivitätsrechnung.

## Datenarchitektur

Drei Ebenen, jede CSV-spezifiziert und gegen Indizes 1-3 des Oberprojekts linkbar: Document Segment (doc_id, doc_type, incumbent_country, target_country, date, competitive_context_flag, history_reference_counts, span_offsets), Source-Year Dyadic (Aggregat pro Quelle/Jahr/Dyade, AS-Score auf dieser Ebene), Country-Year Dyadic (Aggregat pro Incumbent/Target/Jahr, mit EU-Dekomposition). Die EU wird sowohl als nationale Reihen (Deutschland, Frankreich, UK) als auch als Institutionenreihen (EP, Kommission, Rat) geführt, der Komposit explizit gewichtet in `eu_weights_table.csv` (Wortzahl- und Dokumentzahl-Gewichte parallel). Mandatorische Outputs sind neun CSVs plus Replikationsskripte und eine klartext-Methodendokumentation.

## Historische Referenzklassen

Für jedes Incumbent sind die eigenen protektionistischen Episoden als SELF-Klassen taxonomisiert, mit Anker-Termen, Varianten, Zeitfenstern und sprachspezifischen Übersetzungen. Für UK etwa Navigation Acts (1651-1849), Calico Acts (1700 und 1721, 7 Geo. 1 St. 1 c. 7), Corn Laws (Importation Act 1815, 55 Geo. 3 c. 26; Repeal 1846, 9 & 10 Vict. c. 22, Commons 327-229 am 15.5.1846), Fair Trade League (1881-1895), „Made in Germany"-Panik (Merchandise Marks Act 1887, Williams 1896), Tariff Reform (Chamberlain 15.5.1903 Birmingham; Schlaganfall 11.7.1906), Imperial Preference (Import Duties Act 1932, 454-78). Für USA Hamilton Report on Manufactures (5.12.1791), American System (Clay 30.-31.3.1824), McKinley Tariff (1.10.1890, Durchschnitt 38→49,5 Prozent), Smoot-Hawley (17.6.1930), Sematech (1987, Austin, 14 Gründer; 500 Mio. $ autorisiert im NDAA 1988, ca. 870 Mio. $ aufgelaufen bis FY1996 laut CRS, 848 Mio. $ nach DoD-internem Abschlussbericht), CHIPS Act (9.8.2022, 52,7 Mrd. $), COCOM, Toshiba-Kongsberg (acht Maschinen in zwei Tranchen, 17,4 Mio. $ plus 10,7 Mio. $), Section 301 (130 Fälle seit 1974, 35 nach WTO; 2018-Zölle auf ca. 370 Mrd. $ chinesischer Importe). Für Deutschland Friedrich List (1841), Zollverein (Signierung 22.3.1833, in Kraft 1.1.1834), Bismarcks Schutzzollwende (Reichstag 12.7.1879), Universalbanken, Wirtschaftswunder (Währungsreform 20./21.6.1948, Londoner Schuldenabkommen 27.2.1953), Wandel-durch-Handel (Bahr Tutzing 15.7.1963; Scholz-Zeitenwende 27.2.2022). Für Frankreich/EU Colbertismus, Commissariat du Plan (3.1.1946, Monnet; ERP ≈ 20 Prozent der Plan-Investition 1948-52), Nationalisierungswellen (1944-46 und 1981-82, letztere 58 Mrd. Francs), Plan Calcul (19.7.1966, über 100 Mio. $ in fünf Jahren), Airbus (MoU 26.9.1967, GIE 18.12.1970, erster operativer Gewinn 1990), Poitiers-VCR-Affäre (22.10.1982 Fabius-Dekret), EU-Japan Elements of Consensus (31.7.1991, UK 11 Prozent SMMT-JAMA-Deckel). ANALOGY-Klassen umfassen Plaza Accord (22.9.1985, ¥242→¥120), US-Japan-Semiconductor Agreement (2.9.1986, ~20 Prozent Marktanteils-Ziel; DRAM-Anteil Japan 75 Prozent 1987 auf 20 Prozent 2001), VER-Episoden (Japan-US-Auto ab 1.5.1981, 1,68 Mio. Einheiten), GATT-Art.-XXXV-Verweigerungen (Japan-Beitritt 10.9.1955), China-WTO-Beitritt (11.12.2001, Art. 15-Expiry 11.12.2016), Currency-Manipulation-Debatten und Technology-Transfer-Disputes.

## Detektionsstrategie und Normierung

Zwei Schichten, beide protokolliert: Layer 1 deterministisches Anchor Matching mit Fuzzy-Toleranzen, die Spezifikation fordert Levenshtein-Grenzen je nach Termlänge, OCR-Risk-Flag. Layer 2 supervised disambiguation mit stratifiziertem Labelled-Sample für ambige Anker (Hamilton, List, Plaza, Clay); einfaches, auditierbares Modell. Die HRR normalisiert je Dokument auf 1000 Wörter, die Amnesie-Score-Konstruktion läuft über Perzentilnormierung innerhalb Incumbent × doc_type × Dekade (Hauptvariante) und log-cap-Skalierung (Robustheit). Beide Varianten müssen gespeichert werden. Validierung über eine Liste bekannt hochsalienter Episoden (CHIPS Act, Kuka-Übernahme, Poitiers) mit erwarteter Richtung und beobachteten Werten, plus Kohärenzcheck gegen die Indizes 1-3.

## Multilingualität und Pipeline-Vergleich

Original-Sprache primär (Englisch, Deutsch, Französisch, Japanisch), englisch-übersetzte Pipeline parallel, Dokument-Jahr-Flags zeigen welche gemessen hat. Differenzen zwischen beiden sind quantifizierbar und dokumentiert. Japanische Anker (プラザ合意, 日米半導体協定) erfordern Unicode plus MeCab-Tokenisierung, die hier im Schema anzulegen ist.

## Audit-Trajektorie und Methodenlehre

Sieben Runden erzwungen durch den iterativen /verify-Workflow. Runde 1 ersetzte die erste Fassung durch v2.0 (acht Korrekturen, davon eine klare Falschzahl: 397 statt 399 Liberale 1906; eine klare Falschzuordnung: $870M aufgelaufen vs. $500M autorisiert bei Sematech; mehrere Einheitenfehler bei Airbus launch aid, Plan Calcul). Runde 2 hob v2.1 (Wrubel-Zitierung statt falsch attributierter „Frost", Reciprocity of Duties Act 1823 vs. 1822-Enumeration-Trennung). Runde 3 stürzte die Cresson „yellow ants 1989 au Times"-Datierung (v2.2). Runde 4 strich eine nicht belegbare ABC-Chris-Wallace-Zuschreibung (v2.3). Runde 5 identifizierte Rowens WaPo-Op-Ed vom 23.5.1991 als existent, aber nicht korroborierend; schloss vier Residual-Unknowns (v2.4). Runde 6 korrigierte das New-Review-Serialisierungs-Framing von „fünf Installments" auf „sechs von acht Kapiteln, Januar-Juni 1896" (primärquelliches Williams-Preface), markierte den Poitiers-Durchsatz als Einzelquelle (v2.5). Runde 7 bestätigte Stabilität, löste die New-Review-Jahresambiguität (1896 statt 1895) auf, keine weiteren Änderungen. Das methodische Nebenresultat ist die Illustration des /verify-Werts: Ohne iterierte Primärquellenprüfung wären mindestens ein Dutzend zunächst plausibler Angaben als Fakten weitergereicht worden.

## Offen und unsicher

Drei nicht geschlossene Punkte, keiner lasttragend: (1) Die interne Datierung der Japan-Bemerkungen in Schemla, *Édith Cresson: la femme piégée* (Flammarion 1993), bleibt unextrahierbar, der französische-Wikipedia-Verweis auf eine Times-Aussage 1989 ist unbelegt; die englischsprachig belegte erste Primärquelle bleibt Newsweek 26.5.1991. (2) Die monatgenaue Zuordnung der sechs Williams-Kapitel innerhalb New Review Vol. 14 Nr. 80-85 (Januar-Juni 1896) erfordert eine Inhaltsübersicht der sechs Einzelhefte, die aus HathiTrust-Vollsicht-Scans nicht automatisiert lesbar ist. (3) Der Poitiers-Durchsatz 50.000→8.000 Einheiten/Monat ist einziger JAPON-FR-Beleg; CBC gibt 25.000/Woche vor der Maßnahme, Electronics Weekly 53.000 im August 1982 auf rund 1.000 im November 1982 — die ~10x-Größenordnung ist robust, die konkrete Zahl nicht.

Für den praktischen Einsatz der Architektur sind diese drei Punkte Fußnoten. Für eine Publikation mit hohem Reputations-Einsatz wären sie in der ergänzenden Beschaffungsliste (siehe `Beschaffungsliste.md` im Begleitarchiv) prioritär.

## Nächste Schritte am Dokument

Vier nicht erledigte Baustellen, die in /paper oder /data überführt werden könnten: (a) Operationalisierung der Fuzzy-Matching-Schwellenwerte (Levenshtein pro Termlänge, OCR-Fehlermuster), (b) explizite Disambiguierungsregeln für ambige Anker-Terme mit Kontextfenstergrößen, (c) EU-Gewichtungsformel mit dokumentierten Wortzahl- vs. Dokumentzahl-Alternativen, (d) competitive_context_flag-Schwellenwert (boolesch vs. kontinuierlich, Mindesthäufigkeit). Diese waren im Audit Teil C-Reproduzierbarkeitslücken, sind aber Design-Entscheidungen, keine Fakten-Korrekturen; sie gehören in eine Nachfolge-Spezifikationsdatei.

## Quellen

Alle im Chat aufgetretenen Quellen aus den sieben Verifikationsläufen. Flags gelten der Chat-Belegung, nicht der Welt.

**● belegt** Airbus Corporate History (airbus.com), „50th Anniversary of the First Flight of the Airbus A300", Oktober 2022 — https://www.airbus.com/en/newsroom/stories/2022-10-28-october-50th-anniversary-of-the-first-flight-of-the-airbus-a300

**● belegt** American Compass, „Airbus's Industrial Flight Plan" — https://americancompass.org/airbuss-industrial-flight-plan/

**● belegt** Brilliant Maps, „1906 UK Election Map" — https://brilliantmaps.com/uk-elections/1906-uk-election-map/

**● belegt** CBC Archives, „The 'crazy' fight in France over the domestic VCR market in 1982" — https://www.cbc.ca/archives/the-crazy-fight-in-france-over-the-domestic-vcr-market-in-1982-1.5349064

**● belegt** Christian Science Monitor, „Japan disputes US view of damage done by Toshiba sale", 20.7.1987 — https://www.csmonitor.com/1987/0720/osonar.html

**● belegt** Congressional Research Service, R44544, „SEMATECH and U.S. Semiconductor Manufacturing", 27.6.2016 — https://www.congress.gov/crs-product/R44544

**● belegt** Deutsches Historisches Institut Washington / German History in Documents and Images, „E. E. Williams, Made in Germany (1896)" — https://germanhistorydocs.org/en/wilhelmine-germany-and-the-first-world-war-1890-1918/e-e-williams-made-in-germany-1896

**● belegt** DoD Washington Headquarters Services, „SEMATECH 1987-1997: A Final Report to the Department of Defense", 21.2.1997, FOIA 10-F-0709 — https://www.esd.whs.mil/Portals/54/Documents/FOID/Reading%20Room/Science_and_Technology/10-F-0709_A_Final_Report_to_the_Department_of_Defense_February_21_1987.pdf

**● belegt** Dutton, D., „Life Beyond the Political Grave: Joseph Chamberlain, 1906-14", History Today — https://www.historytoday.com/archive/life-beyond-political-grave-joseph-chamberlain-1906-14

**● belegt** Encyclopedia.com, „Workshop of the World" (Oxford Dictionary of Phrase and Fable) — https://www.encyclopedia.com/humanities/dictionaries-thesauruses-pictures-and-press-releases/workshop-world

**● belegt** Grokipedia, „History of Airbus" — https://grokipedia.com/page/History_of_Airbus

**● belegt** HAEU (Historical Archives of the European Union), Fiesole, File FL-713, „Elements of Consensus", Brüssel, 31.7.1991 (Direktzitiert in Milor 2024 JCMS und HBS Working Paper 21-145).

**● belegt** Harvard Business School Working Paper 21-145, „Trade and the Single Car Market: The EC-Japan Elements of Consensus, 1985-1999".

**● belegt** Hansard, „Corn Importation Bill - Adjourned Debate", HC Deb 15 May 1846 vol 86 cc616-727 — https://api.parliament.uk/historic-hansard/commons/1846/may/15/corn-importation-bill-adjourned-debate

**● belegt** Hansard, „Reciprocity of Duties", HC Deb 6 June 1823 — https://api.parliament.uk/historic-hansard/commons/1823/jun/06/reciprocity-of-duties

**● belegt** Hansard (House of Lords), „The EC and Japan ECC Report", 15 November 1989 — https://api.parliament.uk/historic-hansard/lords/1989/nov/15/the-ec-and-japan-ecc-report (Denman-Zitat „workaholics living in rabbit hutches")

**● belegt** HathiTrust Catalog Record 000060795, „The New Review", Vol. 14 = no. 80-85 (1896:Jan.-June), Harvard hvd.hw3qe5 u.a.

**● belegt** Hungerland, W.-F. & Wolf, N. (2022), „The panopticon of Germany's foreign trade, 1880-1913: New facts on the first globalization", *European Review of Economic History* 26(4): 479-507, DOI 10.1093/ereh/heac001.

**● belegt** Internet Archive, Cornell-Kopie cu31924031247830 von Williams, E. E., *Made in Germany* (London: Heinemann 1896), Vorwort Oktober 1896 — https://archive.org/stream/cu31924031247830/cu31924031247830_djvu.txt

**● belegt** JAPON-FR, „Comment la France limitait les importations japonaises de magnétoscopes" — https://japon-fr.com/france-limitait-importations-japonaises-magnetoscopes.htm (Einzelquelle für 50.000→8.000/Monat)

**● belegt** Japan Today / Kuchikomi, Beitrag zur „rabbit hutches"-Zuschreibung an Denman — https://japantoday.com/category/features/kuchikomi/squeezing-into-your-dream-home-in-japan-may-require-some-belt-tightening

**● belegt** LSE Research Online, Harvey, O., „'Hidden' British Protectionism: The Merchandise Marks Act 1887" — https://eprints.lse.ac.uk/113000/1/Harvey_hidden_british_protectionism_published.pdf

**● belegt** Mason, M. (1994), „Elements of Consensus: Europe's Response to the Japanese Automotive Challenge", *JCMS: Journal of Common Market Studies* 32(4): 433-453, DOI 10.1111/j.1468-5965.1994.tb00508.x.

**● belegt** Newsweek, „Hurricane in a Chanel Suit", Online-Fassung mit Published-Date-Metadaten 26.5.1991 — https://www.newsweek.com/hurricane-chanel-suit-204026

**● belegt** Oxford Reference, Oxford Dictionary of Quotations, Disraeli-Eintrag „workshop of the world", Hansard 15.3.1838 — https://www.oxfordreference.com/view/10.1093/acref/9780191826719.001.0001/q-oro-ed4-00003685

**● belegt** People's History Museum, „General Election Trail 1906" — https://phm.org.uk/general-election-trail-1906/

**● belegt** Rowen, H., „France Buttoning Up", *Washington Post*, 23.5.1991 — https://www.washingtonpost.com/archive/opinions/1991/05/23/france-buttoning-up/f8cdf6f1-bd32-43d8-8951-7f0d5377a4d2/ (identifiziert, nicht korroborierend für die „yellow men"-Zitate)

**● belegt** Seattle Times / Boston Globe, Nickerson, C., „'Japanese Are Not Ants' - Sound Trucks Blare Against French Prime Minister", 10.7.1991 — https://archive.seattletimes.com/archive/19910710/1293667/japanese-are-not-ants----sound-trucks-blare-against-french-prime-minister

**● belegt** Semiconductor Industry Association, „Global Semiconductor Sales Increase 6.5% to $439 billion in 2020", 1.2.2021 (Neuffer-Zitat 37→12 Prozent) — https://www.semiconductors.org/global-semiconductor-sales-increase-6-5-to-439-billion-in-2020/

**● belegt** Springer / Vinen, R. (1996), „Trente Glorieuses", in: *France, 1934-1970*, European Studies Series, London, DOI 10.1007/978-1-349-24568-0_8 — https://link.springer.com/chapter/10.1007/978-1-349-24568-0_8

**● belegt** UCL Press / Suzuki, „Europe and the World" (UK 11-Prozent-SMMT-JAMA-Ceiling) — https://journals.uclpress.co.uk/ewlr/article/pubid/EWLR-4-10/

**● belegt** US Government Accountability Office, GAO/RCED-92-283 — https://www.gao.gov/assets/rced-92-283.pdf

**● belegt** Washington College of Law, Digital Commons, Wrubel, W. A. (1989), „The Toshiba-Kongsberg Incident", *American University Journal of International Law and Policy* / später *American University International Law Review* 4(1): 241-273 — https://digitalcommons.wcl.american.edu/cgi/viewcontent.cgi?article=1604&context=auilr

**● belegt** Wikipedia (Chris Wallace Biografie, Golfkrieg 1991) — https://en.wikipedia.org/wiki/Chris_Wallace

**● belegt** Wikipedia (Airbus A310, A300-MoU-Datierung).

**● belegt** Wikipedia (Toshiba-Kongsberg scandal) — ergänzend zur Rekonziliation der Maschinenzahl.

**◐ erwähnt** Asianometry, Jon Y., „Toshiba's Big Technology Export Scandal" — https://www.asianometry.com/p/toshibas-big-technology-export-scandal (Tranchen 17,4 Mio. $ + 10,7 Mio. $)

**◐ erwähnt** Cato Institute / CRS R46604 zu Section 301-Fallzahlen.

**◐ erwähnt** CEPR / VoxEU, Sandkamp et al., „Antidumping Duties, Prices and China" — https://cepr.org/voxeu/columns/antidumping-duties-prices-and-china-free-trade-rescue (51 Prozent der EU-AD-Duties gegen China, 2019, 61 von ~120 Fällen)

**◐ erwähnt** cmtradelaw.com, „Section 301 History and Overview" — https://www.cmtradelaw.com/2025/01/section-301-history-and-overview/ (2018-Zölle 7,5-25 Prozent, ~75 Prozent chinesischer Importe, ~370 Mrd. $)

**◐ erwähnt** Contrepoints, „La bataille de Poitiers de 1982: Fabius contre les magnétoscopes" (Importe im letzten Quartal 1982 „durch 10 geteilt").

**◐ erwähnt** Dissent, „Lessons from the Nationalization Nation" (58 Mrd. Francs 1981-82-Nationalisierung).

**◐ erwähnt** EBSCO Research Starters, Chamberlain-Biografie (11.7.1906-Datierung).

**◐ erwähnt** Electronics Weekly, „The Wittiest Protectionist Measure" (Poitiers 53.000 August → 1.000 November 1982) — https://www.electronicsweekly.com/blogs/mannerisms/yarns/the-wittiest-protectionist-mea-2008-12/

**◐ erwähnt** Fosse.fr, Plan-Calcul-Historie (Allègre-Review nach fünf Jahren) — https://fosse.fr/histoire/plan-calcul-souverainete-numerique.html

**◐ erwähnt** Grokipedia / New World Encyclopedia, Chamberlain (13.7.1906-Minderheitsvariante zurückgewiesen).

**◐ erwähnt** King's College London Project Alpha, Toshiba-Kongsberg Case Study (acht Maschinen in zwei Tranchen).

**◐ erwähnt** Media Fields Journal, „A Business Without a Future: The Parisian Video Club", Poitiers-Episode — https://mediafieldsjournal.org/a-business-without-future/a-business-without-a-future-the-parisian-video-club-past-and.html

**◐ erwähnt** Northwestern Journal of International Law & Business, Toshiba-Kongsberg-Review (zwei Verkaufstranchen MBP-110 vs. MF-Modelle).

**◐ erwähnt** PNAS zu Sematechs 14 Gründungsmitgliedern.

**◐ erwähnt** PIIE (Peterson Institute for International Economics) zum Sematech-Aufgelaufen.

**◐ erwähnt** Spectator (The), Cresson-Newsweek-Zitat-Korroboration.

**◐ erwähnt** UPI Archives, 20.7.1987, Toshiba-Nation-Apology („at least four huge machines") — https://www.upi.com/Archives/1987/07/20/Toshiba-apologizes-to-nation-for-sale-of-submarine-technology/8735553752000/

**◐ erwähnt** Walker, Cardiff, „Voluntary Export Restraints between Britain and Japan" (9-11-Prozent-Band für UK-SMMT-JAMA-Deckel) — https://eastasianbusinesshistory.wordpress.com/wp-content/uploads/2011/07/walker-cardiff2.pdf

**○ ungeprüft** Diamond 1993, Zitation für Marshall, R. (1991), „A Blow Below the Belt", Newsweek 1.7.1991, S. 39 (Homosexualitäts-Zitate aus dem Chris-Wallace-Interview, separat vom „little yellow men"-Zitat).

**○ ungeprüft** Schemla, É. (1993), *Édith Cresson: la femme piégée*, Paris: Flammarion, ISBN 2080668404 (Bibliothekskatalogeinträge verifiziert, Volltext nicht zugänglich; keine Vor-1991-Datierung extrahierbar).

**○ ungeprüft** Cresson, É. (2006), *Histoires françaises*, Monaco/Paris: Éditions du Rocher, ISBN 2268060152 (ebenso).

**○ ungeprüft** Wellesley Index to Victorian Periodicals, Vol. III, Eintrag zu New Review (monatsgenaue Zuordnung der Williams-Kapitel in Vol. 14 nicht auslesbar).

**○ ungeprüft** Hoffmann, W. G. (1965), *Das Wachstum der deutschen Wirtschaft seit der Mitte des 19. Jahrhunderts*, Tab. 126 und 128 (deutsche Export-Werte 1880 und 1913 nicht verbatim extrahiert, aber mit Hungerland/Wolf 2022 konsistent).

*Gesichert aus einem Arbeits-Chat vom 20.11.2026, still geprüft, nicht mit /check auditiert. Flags: ● belegt, ◐ erwähnt, ○ ungeprüft.*
