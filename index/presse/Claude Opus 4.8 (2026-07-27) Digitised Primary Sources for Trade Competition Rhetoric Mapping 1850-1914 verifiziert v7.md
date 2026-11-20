# Digitised Primary Sources for Trade Competition Rhetoric Mapping 1850–1914

**A Verified Source Inventory for Computational Rhetoric Analysis**

Claude (2026)

---

## Scope and Purpose

This inventory maps all confirmed digitally accessible primary sources suitable for systematic frequency measurement of "technology theft," "unfair competition," and related trade rivalry rhetoric across four countries (United Kingdom, United States, Germany, France) between 1850 and 1914. The inventory covers four source categories: parliamentary records, government reports on industry and trade, specialised trade press, and large-scale historical text corpora. Each entry reports access conditions, OCR quality, API availability, and structural bias risks. No estimation: all entries reflect confirmed digitisation status as of early 2026.

The source landscape is deeply asymmetric. English-language parliamentary and newspaper sources offer the strongest infrastructure for computational analysis. German sources face systematic OCR degradation from Fraktur typography. French sources are comprehensive for the Third Republic period (post-1881) but largely inaccessible in full-text form for 1850–1880. Specialised trade press — the genre most likely to contain direct rhetorical escalation — is the least digitised category across all four countries.

---

## 1. Parliamentary Records

Parliamentary debates are the primary category for systematic rhetorical measurement. All four countries have digitised proceedings, but temporal coverage, OCR quality, and machine-readability vary substantially.

### Summary Table: Parliamentary Records

| Quelle | Zeitraum | Land | Volltextzugang | Download | OCR-Qualität | API | Bias-Probleme |
|--------|----------|------|----------------|----------|-------------|-----|---------------|
| Hansard (Historic Hansard) | 1803–2005 | UK | Ja, kostenlos | Bulk (ZIP/XML per Sitzungstag) | Mittel (unkorrigiert) | Ja (pseudo-REST, .js/.opml) | Nicht verbatim; Lücken ca. 4–5% der Volumes; Standing Committees ausgeschlossen |
| Congressional Globe | 1833–1873 | USA | Teilweise (bibliographisch frei; Volltext via HeinOnline kostenpflichtig) | Einzeln (PDF) | Mittel | Teilweise (Congress.gov API v3; kein Bulk für hist. Bände) | Vor 1851 kondensierte Zusammenfassungen, nicht verbatim |
| Congressional Record | 1873–heute | USA | Teilweise (free) / Ja (HeinOnline) | Einzeln (PDF) | Mittel-Hoch | Teilweise | Members dürfen Redetext vor Publikation überarbeiten |
| Reichstagsprotokolle (Stenographische Berichte) | 1867–1942 (Zielzeitraum 1867–1918) | Deutschland | Ja, kostenlos | Bulk (ZIP/XML, vollständiges Korpus) | Mittel (Fraktur, unkorrigiert) | Ja (IIIF via MDZ) | Kein nationales Parlament vor 1867; Preußischer Landtag nur partiell digitalisiert |
| Journal Officiel — Débats parlementaires | 1881–1940 | Frankreich | Ja, kostenlos (Gallica) | Einzeln (PDF); programmatisch via APIs | Mittel (variable OCR-Scores) | Ja (SRU, IIIF, ALTO, OAI-PMH) | Kritische Lücke 1850–1880: Second Empire nur analytische Zusammenfassungen, nicht verbatim |

### Hansard Parliamentary Debates (UK)

**Platform:** https://hansard.parliament.uk/; Bulk-Archive unter https://hansard-archive.parliament.uk/

Vollständig digitalisiert ab 1803. Das UK Parliament stellt ZIP-Archive mit XML-Dateien je Sitzungstag zum Bulk-Download bereit. Die Digitalisierung basiert auf Scans von Printexemplaren, die via OCR verarbeitet wurden; das Parliament bestätigt explizit Tippfehler aus diesem Prozess. Nach Eigenangaben der Digitalisierungsplattform wurden 96% aller verfügbaren Volumes geladen, davon 97% der Informationen erfolgreich übertragen (UK Parliament 2009). Die verbleibenden Lücken betreffen verstreute Einzelbände aller Serien.

Methodisch entscheidend: Hansard ist kein wortgetreues Protokoll. Redundanzen werden gestrichen, Ausdrucksweise geglättet. Standing-Committee-Protokolle sind separat archiviert und nicht systematisch in den Bulk-Daten enthalten. Für die Periode 1850–1914 existiert vollständige Abdeckung der Commons- und Lords-Debatten in frei downloadbaren XML-Dateien.

API-Zugang: Pseudo-REST-API mit JSON- (.js) und OPML-Output durch URL-Extension; TheyWorkForYou-API für neuere Debatten (ab 1918) mit strukturierten Rednerdaten. R-Package `hansard` für programmatischen Zugriff verfügbar.

### Congressional Globe und Congressional Record (USA)

**Platform:** https://www.congress.gov/; HeinOnline (subscription); GovInfo (https://www.govinfo.gov/)

Congressional Globe (1833–1873) und Congressional Record (1873–heute) decken den gesamten Zielzeitraum ab. Die freie Suche auf Congress.gov indexiert nur Seitenüberschriften, keine Volltexte. HeinOnline liefert vollständige Volltextsuche über imagebasierte PDFs mit professioneller Digitalisierungsqualität. Das Congress.gov API v3 (kostenlos, API-Key erforderlich, 5.000 Anfragen/Stunde) sowie GovInfo-API sind primär für moderne Bände ausgelegt; historische gebundene Volumes der Globe-Periode sind nur als Scan-PDFs zugänglich.

Das Globe lieferte bis ca. 1851 kondensierte Zusammenfassungen statt verbatimer Transkriptionen. Der Übergang Globe → Record (1873) erzeugt eine editorische Diskontinuität. Das Record erlaubt Mitgliedern, Redetexte vor Veröffentlichung zu revidieren ("revise and extend remarks"), was die Authentizität als Quelle für Spontanrhetorik einschränkt.

### Reichstagsprotokolle (Deutschland)

**Platform:** https://www.reichstagsprotokolle.de/ (Bayerische Staatsbibliothek); https://www.digitale-sammlungen.de/ (MDZ); GitHub-Korpus: https://github.com/deutschestextarchiv/reichstagsprotokolle

Die vollständigen Stenographischen Berichte des Deutschen Reichstags und seiner Vorläufer (Norddeutscher Bund ab 1867) liegen als frei zugängliches, bulk-downloadbares XML-Korpus im DTA-Basisformat vor. Das Korpus umfasst alle Stenographischen Berichte sowie die Drucksachen (Anlagen, Gesetzesvorlagen, Kommissionsberichte) für den Zeitraum 1867–1942.

OCR-Qualität: Die Bayerische Staatsbibliothek bestätigt ausdrücklich, dass keine Fehlerkorrektur der OCR-Ausgabe vorgenommen wurde (DTA GitHub-Repository). Frakturschrift führt systematisch zu erhöhter Fehlerrate. Für die Vorperiode 1850–1866 existiert auf Bundesebene kein Parlament. Preußische Landtagsprotokolle (Stenographische Berichte ab 1855/56) werden durch den Harald Fischer Verlag partiell kommerziell digitalisiert, aber ohne vollständige Volltextindexierung.

### Journal Officiel — Débats parlementaires (Frankreich)

**Platform:** Gallica, BnF: https://gallica.bnf.fr/

Chambre des députés (61 Jahre verfügbar) und Sénat (60 Jahre verfügbar) sind auf Gallica mit OCR-Text zugänglich. Gallicas APIs (SRU, IIIF Image, Document API für ALTO-XML, OAI-PMH) ermöglichen programmatischen Bulk-Zugriff ohne Registrierung. Jedes Dokument trägt einen OCR-Qualitätsscore (nqamoyen).

Kritische Lücke: Für den Zeitraum 1850–1880 — Second Republic (1848–1851), Second Empire (1852–1870), Übergangsphase (1870–1875) — liegen keine verbatimen Parlamentsprotokolle in digitaler Form vor. Die Annales du Sénat et du Corps législatif dieser Epoche bieten analytische Zusammenfassungen, keine Volltranskriptionen. Der Moniteur universel als offizielles Blatt bis 1868 ist nicht systematisch für Parlamentsdebatten digitalisiert. Erst mit der konsolidierten Dritten Republik (ab ~1881) ist vollständiger Volltextzugang gegeben.

---

## 2. Regierungsberichte zu Industrie, Handel, Patenten und Zollfragen

Regierungsberichte sind ungleichmäßig digitalisiert. UK und USA profitieren von ProQuests umfassender kommerzieller Digitalisierung. Deutsche und französische Quellen sind fragmentierter, aber für die Reichstagsdrucksachen existiert ein hochwertiger Bulk-Zugang.

### Summary Table: Regierungsberichte

| Quelle | Zeitraum | Land | Volltextzugang | Download | OCR-Qualität | API | Bias-Probleme |
|--------|----------|------|----------------|----------|-------------|-----|---------------|
| UK Parliamentary Papers (Blue Books) | 1801–1900 | UK | Ja (ProQuest, kostenpflichtig) | Einzeln (PDF) | Hoch (professionell) | Teilweise (ProQuest-Admin) | Vollständig für Commons; Lords partiell |
| UK Patent Office Annual Reports | 1852–1900 | UK | Teilweise (in Parliamentary Papers) | Einzeln | Mittel | Nein | Nicht eigenständig digitalisiert |
| UK Historical Patents Dataset | 1617–1899 | UK | Ja (GitHub, vollständig) | Bulk (GitHub) | Hoch (strukturierte Daten) | Nein | Keine Rhetorik-Inhalte, nur Patentdaten |
| US Congressional Serial Set + Hearings | 1789–heute | USA | Ja (ProQuest/HeinOnline, kostenpflichtig) | Einzeln (PDF) | Hoch | Teilweise | Variabel nach Modul/Abo |
| US Commissioner of Patents Annual Reports | 1838–1925 (Lücken) | USA | Ja (HathiTrust, kostenlos) | Einzeln (PDF) | Mittel | Ja (HathiTrust Data API) | Lücken in den 1870er Jahren |
| US Commercial Relations with Foreign Countries | 1855–1912 | USA | Ja (HathiTrust) | Einzeln | Mittel | Ja | Titelwechsel; statist. Tabellen OCR-schwach |
| Reichstagsdrucksachen (Anlagen) | 1867–1942 | Deutschland | Ja, kostenlos (MDZ/GitHub) | Bulk (ZIP/XML) | Mittel (Fraktur, unkorrigiert) | Ja (IIIF) | Keine nationale Abdeckung vor 1867 |
| Patentblatt (Kaiserliches Patentamt) | ab 1877/78 | Deutschland | Teilweise (DPMA, PDF-Scans) | Einzeln | Niedrig–Mittel | Teilweise (DPMAregister) | Kein Volltext-OCR für historische Ausgaben bestätigt |
| Statistisches Jahrbuch für das Deutsche Reich | 1880–1942 | Deutschland | Ja (DigiZeitschriften) | Einzeln | Mittel (Fraktur + Tabellen) | Teilweise (PURL) | Beginnt erst 1880 |
| Documents parlementaires (Chambre) | ab ~1881 | Frankreich | Ja (Gallica, teilweise) | Einzeln; programmatisch via APIs | Mittel | Ja (Gallica-APIs) | Vollständigkeit für 1850–1914 nicht gesichert |
| INPI Historical Archives (Patents) | 1791–1901 | Frankreich | Teilweise (bildbasiert) | Einzeln | Niedrig–Unbekannt | Teilweise | Bestand endet 1901 (spätere Patente nicht im historischen Portal); Patentnummer-Suche erst ab 1844; kein OCR-Volltext bestätigt |
| INPI Trademark Archives | 1857–1920 | Frankreich | Teilweise (bildbasiert) | Einzeln | Niedrig–Unbekannt | Teilweise | Digitalisierung 2020–21 abgeschlossen; kein Volltext |
| Tableau général du commerce de la France | 36 Jahrgänge auf Gallica | Frankreich | Ja (Gallica) | Einzeln; programmatisch | Mittel | Ja (Gallica-APIs) | Vollständige Abdeckung 1850–1914 nicht bestätigt |
| UK/DE Handelskammerberichte | 1860–1914 | UK, Deutschland | Nein | Nicht verfügbar | — | — | Nicht digitalisiert; physische Archive |

### UK Parliamentary Papers

**Platform:** https://parlipapers.proquest.com/ (ProQuest)

Die sessional papers des 19. Jahrhunderts (1801–1900) sind vollständig digitalisiert — Volltextsuche und Seitenbilder für jedes Paper —, indexiert nach Cocktons Subject Catalogue of Government Publications. Enthält Board of Trade Reports, Select Committee Reports on Foreign Competition (einschließlich der Royal Commission on the Depression of Trade and Industry 1885–1886), Patent Office Annual Reports, und Zollstatistiken. Professionell digitalisiert von Chadwyck-Healey-Microfiche; OCR-Qualität hoch für Fließtexte, schwächer für statistische Tabellen. Kein offener API.

Für die "Made in Germany"-Debatte der 1880/90er Jahre sind die Sessional Papers zentral: Board of Trade Correspondence, Select Committee Hearings, und die umfangreiche Merchandise Marks Act-Dokumentation sind vollständig enthalten.

### US Patent Office Annual Reports

**Platform:** HathiTrust (https://catalog.hathitrust.org/)

Annual Reports des Commissioner of Patents sind auf HathiTrust für 1838, 1841–1871, 1873, 1876–1919 und 1921–1925 zugänglich; öffentlich-zugängliche Vollansicht für alle Pre-1929-Jahrgänge. Lücken für 1839–1840, 1872 und 1874–1875 bestätigt. Einzeldownload als PDF; Data API und Bibliographic API vorhanden.

### Reichstagsdrucksachen

Die Anlagen zu den Stenographischen Berichten (Drucksachen) sind im selben Bulk-Korpus enthalten wie die Plenarprotokolle (MDZ/GitHub). Für Forschung zur deutschen Handelspolitik, Patentgesetzgebung (1877), Markenrecht (1874, 1894) und Zolltarifen sind diese Quellen direkt zugänglich.

### INPI Historical Archives (Frankreich)

**Platform:** https://data.inpi.fr/; https://www.inpi.fr/en/archives-historiques-INPI

410.000 Erfindungspatente (1791–1901) und 460.000 Markendokumente (1857–1920) wurden digitalisiert (Abschluss Marken: 2020–2021). Zugang ist bildbasiert; kein bestätigter OCR-Volltext. Suchbar nach Patentnummer (ab 1844), Antragstellernamen, Vertreter. Für die quantitative Rhetorikanalyse nicht nutzbar; Wert liegt in der Identifikation von Patentstreitigkeiten und Markenverletzungsfällen als Ereignisdaten.

### Handelskammerberichte (UK und Deutschland)

Nicht digitalisiert. UK Association of Chambers of Commerce: physische Archive im London Metropolitan Archives (CLC/B/016). Deutsche Handelskammern: hochgradig dezentral, Bestände in Dutzenden Regional- und Stadtarchiven. Einige Kammerpublikationen möglicherweise via Google Books-Massendigitalisierung (BSB-Kooperation) zugänglich, aber keine systematische Abdeckung bestätigt. Kammerpetitionen und -eingaben sind partiell in den UK Parliamentary Papers nachvollziehbar.

---

## 3. Industrie- und Handelszeitungen

Die Fachpresse ist die am schwächsten digitalisierte Kategorie. Nur eine Minderheit der zehn untersuchten Titel verfügt über substanzielle, volltextdurchsuchbare digitale Abdeckung für den Zielzeitraum; deutsche Fachblätter sind dabei durchweg schlechter erschlossen als die englisch- und französischsprachigen. Ausgerechnet die Zeitschriften, in denen "Technologiediebstahl"- und "unfair competition"-Rhetorik konzentriert war, sind am schlechtesten zugänglich.

### Summary Table: Industrie- und Handelszeitungen

| Quelle | Zeitraum | Land | Volltextzugang | Download | OCR-Qualität | API | Bias-Probleme |
|--------|----------|------|----------------|----------|-------------|-----|---------------|
| The Economist | 1843–2020 | UK | Ja (Gale, kostenpflichtig) | Einzeln (PDF); Text-Mining-Daten für Institutionen | Hoch (wortkoordinatenbasiert) | Teilweise (Gale Digital Scholar Lab) | Freihandels-liberale Redaktionslinie; repräsentiert London-Perspektive |
| Engineering: An Illustrated Weekly Journal | 1866–heute | UK | Teilweise (einzelne Bände auf IA/HathiTrust) | Einzeln (wo verfügbar) | Niedrig–Mittel (Tesseract, ~21% Seitenvertrauen nachgewiesen) | Nein | Keine systematische Digitalisierung für 1866–1914 |
| Journal of the Society of Chemical Industry | 1882–1929 | UK | Ja (HathiTrust kostenlos pre-1929; Wiley kostenpflichtig) | Einzeln | Mittel (Google-Digitalisierung; Formeln OCR-schwach) | Ja (HathiTrust Data API) | Teil von Vol. 42 auf HathiTrust fehlend |
| Iron and Coal Trades Review | 1858– (Fachblatt) | UK | Teilweise (einzelne Ausgaben auf HathiTrust) | Einzeln (HathiTrust) | Unbekannt | Ja (HathiTrust Data/Bib API) | Keine systematische/vollständige Digitalisierung; nur verstreute Ausgaben; Volltext­abdeckung des Zielzeitraums lückenhaft |
| The Times (London) | 1785–2024 | UK | Ja (Gale Times Digital Archive, kostenpflichtig) | Einzeln; Text-Mining-Daten für Institutionen (XML mit Wortkoordinaten) | Hoch (Mikrofilm-Digitalisierung ab 2002, 1785–1985 bis Ende 2003, konsistent) | Teilweise (Gale) | Nur letzte Londoner Ausgabe (final edition); konservative Redaktionslinie; Mikrofilmschäden |
| Berliner Börsen-Zeitung | 1857–1931 (Lücke 1858–1871) | Deutschland | Teilweise (ZEFYS, bildbasiert; Volltext nicht suchbar) | Einzeln (IIIF/TIFF) | Niedrig–Mittel (wo OCR vorhanden: 70–80% Wortgenauigkeit) | Ja (IIIF, METS) | Lücke 1858–1871 deckt Industrialisierungs- und Einigungsperiode ab; keine Volltextsuche |
| Hamburgischer Correspondent | 1712–1934 digitalisiert (SUB Hamburg) | Deutschland | Ja (Volltext-OCR 1905–1934 gesichert; Jg. 1712–1904 nachträglich OCR-erschlossen, ca. 463.000 S.) | Einzeln | Mittel (Fraktur ca. 70–85%) | Ja (IIIF; Europeana; DDB) | 1905 mit Hamburger Börsenhalle fusioniert; national-liberal, regierungsnah |
| Export: Organ des Centralvereins für Handelsgeographie | 1879–1881 (einzelne Bde.), 1912 | Deutschland | Teilweise (Google Books, IA) | Einzeln (verfügbare Bde.) | Niedrig–Mittel | Nein | Nahezu vollständige Digitalisierungslücke für eine der direkt relevantesten deutschen Quellen |
| Journal des économistes | 1841–ca. 1940 | Frankreich | Ja, kostenlos (Gallica; 81 Jahrgänge verfügbar) | Einzeln; programmatisch via Gallica-Tools | Mittel–Hoch (Gallica OCR-Scores; franz. Typographie 19. Jh. generell gut) | Ja (SRU, IIIF, OAI-PMH; keine Registrierung) | Klassisch-liberale, freihandels-orientierte Redaktionslinie |
| L'Économiste français | 1873–ca. 1940 | Frankreich | Ja, kostenlos (Gallica; 66 Jahre); RetroNews (erweitert, kostenpflichtig) | Einzeln; programmatisch | Mittel–Hoch | Ja (Gallica-APIs) | Beginnt erst 1873; Leroy-Beaulieu liberal-kolonialpolitische Linie |

### The Economist Historical Archive

**Platform:** Gale Primary Sources; HathiTrust (Bände 1–111, ca. 1843–1930, mit zahlreichen Lücken); Internet Archive

Vollständige Abdeckung aller Ausgaben seit der Gründung 1843. Professionelle Digitalisierung von Mikrofilm mit wortkoordinatenbasierter OCR-Kodierung, die Phrasensuche mit hoher Präzision ermöglicht. Für institutionelle Text-Mining-Lizenzen stellt Gale Digital Scholar Lab XML-Rohdaten mit Wortkoordinaten auf physischen Laufwerken bereit. Keine offene REST-API. Redaktionslinie: ausgeprägt freihandelsliberal, was protektionistische und "Technologiediebstahl"-Rhetorik als berichteten Gegendiskurs, nicht als eigene Position enthält.

### The Times Digital Archive

**Platform:** Gale Primary Sources: https://www.gale.com/c/the-times-digital-archive

Vollständige Abdeckung 1785–2024. Die Digitalisierung begann 2002 durch Scannen des bestehenden 35-mm-Mikrofilms; der Grundbestand 1785–1985 wurde bis Ende 2003 in nur zwei Jahren mit durchgängig konsistenter Ausstattung und Methodik erfasst, was gleichmäßige Bild- und OCR-Qualität sichert. Volltextsuchbar; 26 Inhaltssubkategorien. Text-Mining-Daten (XML mit Wortkoordinaten, DTD bereitgestellt) für Institutionen auf Anfrage. OCR-Qualität hoch, aber durch Mikrofilmschäden (Knicke, Risse) partiell beeinträchtigt. Der Mikrofilm bewahrt jeweils die letzte Londoner Ausgabe (final edition); Regionalausgaben (etwa irische oder schottische) fehlen vollständig.

### Engineering: An Illustrated Weekly Journal

**Platform:** Internet Archive (https://archive.org/); HathiTrust (einzelne Bände)

Keine systematische Digitalisierung für 1866–1914 bestätigt. Einzelne Jahrgänge (z.B. 1868, 1918) sind als Tesseract-OCR-Digitalisate auf Internet Archive zugänglich, in wechselnder, insgesamt geringer Qualität. Die IA-Metadaten weisen für einzelne Bände niedrige Konfidenzwerte aus (z.B. Seitenzahl-Erkennung 21,22; Skript-Konfidenz rund 0,67); für systematische Rhetorikanalyse ist der Bestand nicht zuverlässig nutzbar.

### Export: Organ des Centralvereins für Handelsgeographie

**Platform:** Internet Archive; Google Books; Wikisource-Listing

Jene Zeitschrift, die als direktes Organ des Centralvereins für Handelsgeographie die deutsche Handelsexpansionsrhetorik am konzentriertesten dokumentiert haben dürfte, ist nahezu vollständig undigitalisiert. Verfügbare Bände: 1879–1881 (Vols. 1–3) via Google Books sowie ein Jahrgang 1912 auf Internet Archive. Der Zeitraum 1882–1911 fehlt vollständig in digitaler Form.

### Journal des économistes

**Platform:** Gallica, BnF: https://gallica.bnf.fr/ark:/12148/cb34426009k/date

81 Jahrgänge auf Gallica verfügbar, mit OCR-Text (dokumentierte Erkennungsrate einzelner Bände um 97%). Vollständige Gallica-API-Suite ohne Registrierung: SRU-Suche, Document API (ALTO-XML per Seite), IIIF-Image-API, ContentSearch (wortstufige Suche innerhalb von Dokumenten), OAI-PMH. Python-Wrapper (PyGallica, gallipy) verfügbar. Redaktionslinie: Flaggschiff der französischen klassischen Liberalökonomie (Guillaumin-Verlag); Bastiat, Walras, Pareto, Molinari als Beiträger. Protektionistische Rhetorik erscheint als berichteter Gegendiskurs.

---

## 4. Historische Textkorpora

Die drei internationalen Makrokorpora (Google Books Ngram, HathiTrust, Internet Archive) bieten komplementäre Stärken. Nationale Digitalbibliotheken füllen kritische Lücken, wobei Gallica und Chronicling America die stärkste Open-Access-Infrastruktur aufweisen.

### Summary Table: Historische Textkorpora

| Quelle | Zeitraum | Land/Sprache | Volltextzugang | Download | OCR-Qualität | API | Bias-Probleme |
|--------|----------|-------------|----------------|----------|-------------|-----|---------------|
| Google Books Ngram Corpus | 1800–2022 | EN, DE, FR u.a. | Nein (nur Frequenzdaten; Snippets via Google Books) | Bulk (N-Gramm-Frequenz-TSVs, CC-BY 3.0); BigQuery | Mittel (Pre-1800 problematisch; Long-s-Fehler) | Teilweise (keine offiz. REST-API; BigQuery; Python-Libs) | Bücher only; kein Periodikum; zunehmend Wissenschaftsliteratur post-1900; Korpuszusammensetzung zeitlich variabel; Metadatenfehler dokumentiert |
| HathiTrust Digital Library | 1500–heute | Multilingual (~50% EN) | Teilweise (>6,5 Mio. Public-Domain-Bde. Vollansicht; 1850–1914 fast vollständig PD) | Bulk (HTRC Extracted Features v2.0, 17,1 Mio. Bde., 4 TB komprimiert, via rsync) | Mittel–Niedrig (Google-Digitalisierung; Fraktur stark beeinträchtigt) | Ja (Data API, Bibliographic API, TORCHLITE) | US-Forschungsbibliotheken überrepräsentiert; Bag-of-Words (keine Phrasenkonstruktion); HTRC-Förderung endet 2026 |
| Internet Archive | Alle Perioden | Multilingual (EN dominant) | Ja (Public Domain) | Bulk (ia-CLI; DJVU-XML mit Wortkoordinaten; Multiple Formate) | Niedrig–Mittel (~78% Wortgenauigkeit; Fraktur praktisch unlesbar; Spaltenverwirrung bei Zeitungen) | Ja (Python-CLI; S3-API; Item-Metadata-API; Advanced Search API) | Metadatenfehler; Duplikate häufig; Fraktur nicht automatisch lesbar; Zeitungskolumnen-OCR-Probleme |
| British Newspaper Archive (BNA) | 1720–1950er | UK (EN) | Ja, Volltextsuche (Viewing: Abo; ~6 Mio. Seiten kostenlos pre-1909) | Keine Bulk-Option; kein API | Mittel–Niedrig (ca. 78% Wortgenauigkeit, 83,6% Zeichengenauigkeit) | Nein | Geographische Konzentration London/Midlands; spezialisierte Fachpresse unterrepräsentiert; kein API schließt Bulk-Analyse aus |
| British Library Digital Collections | Vielfältig | UK (EN) | Variabel (60.000+ Bde. Public Domain kostenlos via Microsoft; Making of the Modern World II: Abo) | Variabel | Mittel (60–85% Wortgenauigkeit für Zeitungen) | Teilweise | Selektive Digitalisierung; meiste relevanten wirtschafts-/handelspolitischen Quellen Abo-pflichtig |
| ZEFYS (Staatsbibliothek Berlin) | Variabel (222 Titel, >628.000 Ausgaben) | Deutschland (DE) | Eingeschränkt (Volltextsuche nur für Amtspresse Preußens und DDR-Presse; allg. Zeitungssammlung: Browse only) | Einzeln (IIIF, TIFF/JPG); ALTO-XML für Einzeltitel | Niedrig–Mittel (70–80% Wortgenauigkeit wo OCR; Fraktur) | Ja (IIIF; METS-XML) | Starke Berlin/Preußen-Konzentration; kein allgemeiner Volltext-Such-API |
| Deutsches Textarchiv (DTA) | ca. 1600–1900 | Deutschland (NHG) | Ja, kostenlos | Bulk (XML/TEI-P5, HTML, TCF, Plaintext; CC BY-NC) | Sehr hoch (99,9%+ Zeichengenauigkeit via Double Keying; 350 Mio. Tokens, 1,34 Mio. Seiten) | Ja (OAI-PMH, OpenSearch, CAB-API, Atom) | Endet bei ca. 1900 — kein Zugang zu 1900–1914; linguistisch, nicht thematisch selektiert; ~3.200+ Texte |
| Gallica (BnF) | Mittelalter–20. Jh. | Frankreich (FR) | Ja, kostenlos (10 Mio. Dokumente, davon ~5,8 Mio. Zeitungen und Periodika) | Einzeln; programmatisch via APIs (ALTO-XML, IIIF, SRU) | Mittel (variable OCR-Scores; qualitative Unterschiede nach Epoche) | Ja (SRU, IIIF, Document API, ContentSearch, OAI-PMH; keine Registrierung) | Frankophone Ausrichtung; nicht alle BnF-Bestände digitalisiert; RetroNews-Erweiterfunktionen Abo-pflichtig |
| Chronicling America (LoC) | 1756–1963 | USA (EN + weitere) | Ja, kostenlos; Volltext durchsuchbar | Bulk (METS/ALTO-XML; OCR-Plaintext; JPEG2000; Rate Limit: 10 Bulk-Anfragen/10 Min.) | Mittel (ca. 70–85% Wortgenauigkeit; variabel nach Bundesstaat und Digitalisierungsjahr) | Ja (loc.gov JSON-API; OpenSearch; METS/ALTO; Linked Data; Jupyter Notebooks; kostenlos, kein Key) | Überrepräsentation "papers of record"; NYT, WSJ, Chicago Tribune NICHT enthalten (kommerzielle DBs); Fachpresse unterrepräsentiert; 4.000+ Titel, >24 Mio. Seiten (Stand Feb. 2024) |

### Google Books Ngram Corpus

**Platform:** https://books.google.com/ngrams; http://storage.googleapis.com/books/ngrams/books/datasetsv3.html; Google BigQuery

Englisch-, Deutsch- und Französischkorpora abdeckend. N-Gramm-Frequenzdaten als komprimierte TSV-Dateien bulk-herunterladbar (CC-BY 3.0). Threshold: nur N-Gramme mit ≥40 Vorkommen im Korpus eingeschlossen. Keine API für Volltextzugriff; nur Frequenzdaten. Entscheidende methodische Einschränkung: Zeitschriften, Zeitungen und Parlamentsprotokolle sind nicht enthalten — das Korpus erfasst ausschließlich Bücher. Pechenick et al. (2015) dokumentieren eine zunehmende Dominanz wissenschaftlicher Literatur im 20.-Jahrhundert-Korpus, die Makrotrends verzerrt. Koplenig (2017) weist Diskontinuitäten im deutschen Korpus nach. Long-s-Fehler beeinträchtigen Pre-1800-Bestände; für 1850–1914 geringer.

### HathiTrust Digital Library und HTRC

**Platform:** https://www.hathitrust.org/; https://analytics.hathitrust.org/

Über 18 Millionen Volumes; für Pre-1929-Material (US-Urheberrecht) vollständige Ansicht kostenlos. Der HTRC Extracted Features Dataset v2.0 (17,1 Mio. Volumes, Snapshot Februar 2020, 4 TB komprimiert, via rsync) stellt page-level POS-getaggte Token-Counts für alle Volumes bereit — sowohl Public Domain als auch urheberrechtlich geschützte Werke. Für 1850–1914 sind nahezu alle Materialien Public Domain. Die Token-Daten sind Bag-of-Words: Phrasenrekonstruktion ist nicht möglich. Frakturgedrucktes deutsches Material ist erheblich OCR-beeinträchtigt. Hinweis: HTRC-Förderung endet 2026, was Kontinuität der Infrastruktur betrifft.

### Deutsches Textarchiv (DTA)

**Platform:** https://www.deutschestextarchiv.de/

Qualitativ überragendes Korpus für Neuhochdeutsch 1600–1900, produziert durch Double-Keying (manuelle Zweifach-Transkription; garantierte Zeichengenauigkeit ≥99,9%). Aktuell über 3.200 Texte mit mehr als 350 Millionen Tokens auf 1,34 Millionen digitalisierten Seiten (Kernkorpus und DTA-Erweiterungskorpus zusammen; Stand nach CLARIN-Daten) (Geyken et al. 2018). Vollständig bulk-downloadbar in XML/TEI-P5, HTML, TCF und Plaintext unter CC-BY-NC. Linguistische Annotation: Tokenisierung, Lemmatisierung, POS-Tagging, historische Orthographienormalisierung.

Entscheidende Einschränkung für die Forschungsfrage: Die temporale Obergrenze liegt bei ca. 1900. Die kritische Periode 1900–1914 — in der die "Made in Germany"-Debatte ihren zweiten Höhepunkt erreichte und die Rhetorik vor dem Ersten Weltkrieg eskalierte — ist vollständig ausgeschlossen. Die Textauswahl folgt linguistischen, nicht thematischen Kriterien, was wirtschafts- und handelspolitische Texte nicht bevorzugt.

### Chronicling America (Library of Congress)

**Platform:** https://www.loc.gov/collections/chronicling-america/ (ab August 2025 neue URL)

Umfang (Stand Februar 2024): über 24 Millionen Seiten, über 4.000 Zeitungstitel aus allen US-Bundesstaaten und Territorien, Zeitraum 1756–1963 (Robertson Library 2024). Vollständig kostenloser Volltextzugriff ohne API-Key. Die loc.gov JSON-API, OpenSearch, METS/ALTO-XML und Linked-Data-Endpunkte sind ohne Registrierung zugänglich; sechs offizielle Jupyter-Notebooks für API-Nutzung verfügbar. Bulk-OCR-Download mit Rate-Limit (10 Anfragen/10 Minuten pro IP).

Methodische Einschränkung: Die großen nationalen Tageszeitungen (New York Times, Wall Street Journal, Chicago Tribune) sind nicht enthalten — sie liegen in kommerziellen Datenbanken. Die Selektion favorisiert regionale Gemeindeblätter. Fachpresse und Handelsblätter sind unterrepräsentiert. Für die spezifische Frage nach US-Rhetorik über deutsche und britische Konkurrenz bietet Chronicling America dennoch die breiteste frei zugängliche Abdeckung.

### ZEFYS (Zeitungsinformationssystem, Staatsbibliothek Berlin)

**Platform:** https://zefys.staatsbibliothek-berlin.de/

222 Zeitungstitel, über 628.000 Ausgaben, darunter Vossische Zeitung, Volks-Zeitung (1853–1904), National-Zeitung (1840–1918), Königlich privilegirte Berlinische Zeitung. Wichtig: Volltextsuche ist nur für die Untersammlungen Amtspresse Preußens und DDR-Presse verfügbar; die allgemeine Zeitungssammlung unterstützt nur datumbasiertes Browsing — die OCR-Daten (~50% der Titel) sind nicht suchbar freigeschaltet. ALTO-XML-OCR für einzelne Titel (Norddeutsche Allgemeine Zeitung, Provinzial-Correspondenz, Neueste Mittheilungen) downloadbar. IIIF-Protokoll für Bilder; METS-Metadaten in XML. Starke Berlin/Preußen-Konzentration.

---

## Forschungsdesign-Implikationen

Die Quellenlandschaft erzwingt ein sprachlich asymmetrisches Forschungsdesign. Für englischsprachige Quellen ist systematische Frequenzmessung technisch realisierbar: Hansard-XML-Bulk + Chronicling America + The Economist (Gale) + The Times Digital Archive ermöglichen computational rhetoric analysis mit OCR-Qualitäten zwischen 70% und >90% Wortgenauigkeit.

Für deutschsprachige Quellen ist Fraktur das strukturelle Hindernis. Das Deutsches Textarchiv bietet überlegene Textqualität, endet aber bei 1900. Die Reichstagsprotokolle als Bulk-Korpus sind die einzige frei zugängliche deutsche Quelle mit breiter zeitlicher Abdeckung und akzeptabler (wenn auch unkorrigierter) OCR. Für deutsche Fachpresse existiert kein systematisch nutzbarer digitaler Bestand.

Für französischsprachige Quellen bietet Gallica die technisch ausgereifteste offene API-Infrastruktur; aber die Abdeckung vor 1881 ist für parlamentarische Quellen strukturell nicht behebbar ohne Einbeziehung physischer Archive.

Die empfohlene Quellenkombination nach Forschungsziel:

**Parlamentarische Rhetorik:** Hansard-Bulk-XML (kostenlos) + Reichstagsprotokolle-Bulk-XML (kostenlos) + Journal Officiel via Gallica-APIs (kostenlos, ab 1881)

**Pressediskurs:** The Economist und The Times (Gale, Abo) + Journal des économistes via Gallica (kostenlos) + Chronicling America (kostenlos, API)

**Breitenvalidierung:** Google Books Ngram (kostenlos, Bücher only) + HathiTrust Extracted Features (kostenlos, Bag-of-Words)

**Spezifischer Bias-Hinweis:** Keine der identifizierten Quellen erfasst Handelskammerrhetorik systematisch in digitaler Form. Diese Lücke betrifft eine der institutionell wichtigsten Kanäle organisierter Wirtschaftslobbyarbeit zu Schutzrechts- und Wettbewerbsfragen.

---

## Literaturverzeichnis

Bayerische Staatsbibliothek (2024) *Reichstagsprotokolle — Verhandlungen des Deutschen Reichstags und seiner Vorläufer inklusive Datenbank der Reichstagsabgeordneten*. Munich: Münchner Digitalisierungszentrum. Available at: https://www.digitale-sammlungen.de/de/reichstagsprotokolle-verhandlungen-des-deutschen-reichstags-und [Accessed: January 2026].

Bibliothèque nationale de France (2024) *Gallica: Bibliothèque numérique de la BnF et de ses partenaires*. Paris: BnF. Available at: https://gallica.bnf.fr/ [Accessed: January 2026].

Bibliothèque nationale de France (2024) *API Document de Gallica*. Paris: BnF. Available at: https://api.bnf.fr/fr/api-document-de-gallica [Accessed: January 2026].

British Library (2025) *British Newspaper Archive*. London: British Library / FindMyPast. Available at: https://www.britishnewspaperarchive.co.uk/ [Accessed: January 2026].

Deutsches Textarchiv (DTA) (2024) *Deutsches Textarchiv — Zweitveröffentlichungsserver der BBAW*. Berlin-Brandenburgische Akademie der Wissenschaften. Available at: https://www.deutschestextarchiv.de/ [Accessed: January 2026].

Gale (2024) *The Times Digital Archive, 1785–2024*. Farmington Hills: Gale, a Cengage Company. Available at: https://www.gale.com/c/the-times-digital-archive [Accessed: January 2026].

Gale (2024) *The Economist Historical Archive*. Farmington Hills: Gale, a Cengage Company. Available at: https://www.gale.com/c/the-economist-historical-archive [Accessed: January 2026].

Geyken, A., Boenig, M., Haaf, S., Jurish, B., Thomas, C. and Wiegand, F. (2018) 'Das Deutsche Textarchiv als Forschungsplattform für historische Daten in CLARIN', in Lobin, H., Schneider, R. and Witt, A. (eds.) *Digitale Infrastrukturen für die germanistische Forschung*. Berlin/Boston: De Gruyter, pp. 219–248.

HathiTrust Digital Library (2025) *HathiTrust Digital Library*. Ann Arbor: HathiTrust. Available at: https://www.hathitrust.org/ [Accessed: January 2026].

HathiTrust Research Center (2025) *HTRC Extracted Features Dataset v2.0*. Urbana-Champaign: University of Illinois. Available at: https://analytics.hathitrust.org/ [Accessed: January 2026].

Institut National de la Propriété Industrielle (INPI) (2024) *INPI Historical Archives Online*. Paris: INPI. Available at: https://www.inpi.fr/en/archives-historiques-INPI [Accessed: January 2026].

Kampkaspar, D. (2017) 'Review of "Deutsches Textarchiv"', *RIDE*, 6. DOI: https://doi.org/10.18716/ride.a.6.8.

Koplenig, A. (2017) 'The impact of lacking metadata for the measurement of cultural and linguistic change using the Google Ngram data sets — Reconstructing the composition of the German corpus in times of WWII', *Digital Scholarship in the Humanities*, 32(1), pp. 169–188.

Library of Congress (2025) *Chronicling America: Historic American Newspapers*. Washington, D.C.: Library of Congress / National Endowment for the Humanities. Available at: https://www.loc.gov/collections/chronicling-america/ [Accessed: January 2026].

Michel, J.-B., Shen, Y. K., Aiden, A. P., Veres, A., Gray, M. K., Brockman, W., The Google Books Team, Pickett, J. P., Hoiberg, D., Clancy, D., Norvig, P., Orwant, J., Pinker, S., Nowak, M. A. and Aiden, E. L. (2011) 'Quantitative analysis of culture using millions of digitized books', *Science*, 331(6014), pp. 176–182.

Pechenick, E. A., Danforth, C. M. and Dodds, P. S. (2015) 'Characterizing the Google Books corpus: Strong limits to inferences of socio-cultural and linguistic evolution', *PLOS ONE*, 10(10), e0137041. DOI: https://doi.org/10.1371/journal.pone.0137041.

ProQuest (2024) *UK Parliamentary Papers: 19th Century House of Commons Sessional Papers*. Ann Arbor: ProQuest LLC. Available at: https://parlipapers.proquest.com/ [Accessed: January 2026].

ProQuest (2024) *ProQuest U.S. Congressional Collection*. Ann Arbor: ProQuest LLC. Available at: https://about.proquest.com/en/products-services/proquest-congressional/ [Accessed: January 2026].

Robertson Library, University of Prince Edward Island (2024) *Chronicling America: Historic American Newspapers*. Available at: https://libraryupei.ca/chronicling-america-historic-american-newspapers [Accessed: January 2026].

Staatsbibliothek zu Berlin (2024) *ZEFYS — Zeitungsinformationssystem*. Berlin: Stiftung Preußischer Kulturbesitz. Available at: https://zefys.staatsbibliothek-berlin.de/ [Accessed: January 2026].

UK Parliament (2009) *Hansard 1803–2005: Volumes Index*. London: UK Parliament. Available at: https://api.parliament.uk/historic-hansard/volumes/index.html [Accessed: January 2026].

UK Parliament (2024) *Hansard Archive (digitised debates from 1803)*. London: UK Parliament. Available at: https://hansard-archive.parliament.uk/ [Accessed: January 2026].

Wikipedia (2026) *Chronicling America*. Available at: https://en.wikipedia.org/wiki/Chronicling_America [Accessed: January 2026].
