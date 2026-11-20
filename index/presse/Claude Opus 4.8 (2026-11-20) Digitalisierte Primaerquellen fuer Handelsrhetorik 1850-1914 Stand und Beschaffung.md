# Digitalisierte Primärquellen für Handelsrhetorik 1850-1914, Stand und Beschaffung

*Dieser Chat hat kartiert, mit welchen digitalen Quellen sich „Technologiediebstahl"- und „unfair competition"-Rhetorik in UK, USA, Deutschland und Frankreich zwischen 1850 und 1914 maschinell messen lässt, und den Befund über acht Prüfrunden belastbar gemacht.*

## Kernpunkte
1. Die Kartierung erfasst 42 digitalisierte Quellen in vier Gruppen (Parlamentsprotokolle, Regierungsberichte, Fachpresse, Großkorpora); für alle vier Länder sind Parlamentsdebatten volltextlich zugänglich, aber deutsche Quellen leiden unter Fraktur-OCR, und französische Debatten fehlen volltextlich vor 1881.
2. Die Fachpresse ist die schwächste Gruppe: Engineering, die Iron and Coal Trades Review und das Export-Organ des Centralvereins für Handelsgeographie sind kaum oder gar nicht digitalisiert, also ausgerechnet dort, wo diese Rhetorik am dichtesten saß.
3. Die stärkste maschinell nutzbare Infrastruktur ist englischsprachig, vor allem Hansard als Bulk-XML und Chronicling America mit über 24 Millionen Seiten und freier API; das Deutsche Textarchiv bietet 99,9 Prozent Zeichengenauigkeit, endet aber bei 1900 und lässt damit die Vorkriegsjahre 1900-1914 aus (Geyken et al. 2018).
4. Acht Prüfrunden haben rund fünfzehn Sachangaben korrigiert, darunter das HathiTrust-Extracted-Features-Datenpaket (v2.0 mit 17,1 Millionen Bänden, nicht v2.5 mit 18,7 Millionen), die Reichstagsprotokolle (1867-1942 statt nur bis 1918) und die Economist-Bände auf HathiTrust (1-111 statt 1-109); die Fassung ist jetzt stabil.
5. Vierzehn Quellen müssen beschafft oder freigeschaltet werden, teils kostenpflichtige Datenbanken (Gale, ProQuest, HeinOnline), teils undigitalisierte Periodika und Archive (Handelskammerberichte, Export, INPI als reine Bildscans).

## Was die Kartierung ergab
Die vier Länder lassen sich auf Parlamentsebene durchgängig erfassen. Hansard liegt ab 1803 als frei herunterladbares XML je Sitzungstag vor; das US-Pendant aus Congressional Globe (bis 1873) und Congressional Record deckt den ganzen Zeitraum, der Volltext aber nur gegen Gebühr über HeinOnline. Die deutschen Reichstagsprotokolle sind als vollständiges Bulk-XML-Korpus 1867-1942 offen, die OCR jedoch unkorrigiert und durch Fraktur geschwächt. Frankreichs Journal Officiel ist über Gallica mit offenen Schnittstellen abrufbar, aber erst ab etwa 1881; die Jahre 1850-1880 fehlen volltextlich.

Bei den Großkorpora trägt die englischsprachige Seite am weitesten. Chronicling America bietet über 24 Millionen Zeitungsseiten frei und per API (Stand Februar 2024), die Gale-Archive von Economist (1843-2020) und Times (1785-2024) liefern wortkoordinatengenaue OCR, aber nur im Abo. Google Books Ngram zählt nur Bücher, keine Periodika, und nimmt nur N-Gramme mit mindestens 40 Vorkommen auf (Michel et al. 2011). Das HathiTrust Extracted Features Dataset v2.0 stellt für 17,1 Millionen Bände seitenweise Token-Zählungen bereit, allerdings als Bag-of-Words ohne Phrasenrekonstruktion.

Die empfohlene Quellenkombination fasst der folgende Auszug zusammen (im Chat hergeleitet):

| Zweck | Quelle | Zugang |
|---|---|---|
| Parlamentsrhetorik | Hansard Bulk-XML | frei, Download |
| Parlamentsrhetorik | Reichstagsprotokolle 1867-1942 | frei, Bulk-XML |
| Parlamentsrhetorik | Journal Officiel ab 1881 (Gallica) | frei, API |
| Pressediskurs | The Economist / The Times (Gale) | Abo |
| Pressediskurs | Journal des économistes (Gallica) | frei, API |
| Pressediskurs | Chronicling America | frei, API |
| Breitentrend | Google Ngram, HathiTrust Extracted Features | frei |

Die vollständige Kartierung mit allen 42 Einträgen, OCR-Qualitäten, API-Angaben und Bias-Hinweisen liegt im beigelegten Arbeitsdokument (ZIP, `… verifiziert v7.md`).

## Was die acht Prüfrunden geändert haben
Jede Runde hat die jeweils letzte Fassung erneut gegen die Primärquellen geprüft und die Versionsnummer hochgezählt, bis nichts mehr zu korrigieren war. Korrigiert wurden unter anderem: die Seitenzahl des Journal des économistes (nicht belegbar, entfernt) und die INPI-Lücke (Bestand endet 1901, kein Sprung bis 1977); der Hamburgische Correspondent (Volltext 1905-1934 gesichert, Jahrgänge 1712-1904 nachträglich OCR-erschlossen); das HathiTrust-Datenpaket (v2.0, 17,1 Millionen Bände); Zeitraum und Edition der Times (ab 2002, Grundbestand bis Ende 2003; letzte Londoner Ausgabe statt Abendausgabe); die Engineering-OCR-Kennzahl (21,22 ist die Seitenzahl-Erkennung, nicht die Textgüte); die Iron and Coal Trades Review (entgegen der ersten Angabe teilweise auf HathiTrust); die UK-Parliamentary-Papers-Seitenzahl (nicht belegbar, ersetzt), die Gallica-Zeitungsangabe (rund 5,8 Millionen Dokumente, keine Seiten) und die Economist-Bände auf HathiTrust (1-111 bis 1930); schließlich der Reichstags-Zeitraum (1867-1942). Runde acht fand keine Korrektur mehr; die Fassung v7 ist stabil.

## Was noch zu beschaffen ist
Vierzehn Quellen sind nicht frei prüfbar und müssen freigeschaltet oder physisch beschafft werden. Kostenpflichtig über Anbieter: HeinOnline (Congressional Record und Globe im Volltext), ProQuest (UK Parliamentary Papers; U.S. Congressional Collection), Gale (Economist Historical Archive; Times Digital Archive; Making of the Modern World Part II) und British Newspaper Archive (Abo, kein Bulk/API). Nicht oder nur verstreut digitalisiert und darum physisch bzw. über Mikrofilm zu holen: Engineering (1866-1914), Iron and Coal Trades Review (19.-Jh.-Lauf), Export des Centralvereins (Jahrgänge 1882-1911), die Berliner Börsen-Zeitung (nur Bilddigitalisat, keine Volltextsuche), die UK Chamber of Commerce reports (London Metropolitan Archives, Bestand CLC/B/016) und die deutschen Handelskammerberichte (dezentral in Regional- und IHK-Archiven). Als Datensatz ohne Volltext-OCR: die INPI-Archives historiques (Patente 1791-1901, Marken 1857-1920, reine Bildscans, nicht text-mining-fähig). Die vollständige Beschaffungsliste mit kopierfertigen Suchbegriffen steht im Chat über dieser Sicherung.

## Offen und unsicher
Der Volltext hinter den Abo-Datenbanken (Gale, ProQuest, HeinOnline) ließ sich nicht aus erster Hand prüfen; bestätigt ist nur die anbieterdokumentierte Abdeckung, nicht die OCR-Güte im Inneren. Berliner Börsen-Zeitung und INPI liegen bildbasiert vor, für Frequenzmaße braucht es dort eigene OCR. Die Handelskammerberichte sind gar nicht digitalisiert; ob der Aufwand einer Archivbeschaffung sich lohnt, ist eine Forschungsentscheidung, keine Quellenfrage. Anzumerken ist, dass die Prüfrunden im Chat irrtümlich auf den 27.07.2026 datiert wurden; tatsächlich lief die Arbeit am 20.11.2026, worauf diese Sicherung datiert ist. Der Dateiname des Arbeitsdokuments trägt noch das falsche Datum (2026-07-27), inhaltlich ist es die stabile Fassung.

## Quellen
● Chronicling America (Library of Congress). Historic American Newspapers. https://www.loc.gov/collections/chronicling-america/

◐ Geyken, A., Boenig, M., Haaf, S., Jurish, B., Thomas, C. und Wiegand, F. (2018). Das Deutsche Textarchiv als Forschungsplattform für historische Daten in CLARIN. In: Lobin, H., Schneider, R. und Witt, A. (Hrsg.), Digitale Infrastrukturen für die germanistische Forschung. Berlin/Boston: De Gruyter, S. 219-248.

● HathiTrust Research Center (2020). Extracted Features Dataset v2.0. https://analytics.hathitrust.org/

◐ Koplenig, A. (2017). The impact of lacking metadata for the measurement of cultural and linguistic change using the Google Ngram data sets. Digital Scholarship in the Humanities, 32(1), S. 169-188.

◐ Michel, J.-B., Shen, Y. K., Aiden, A. P. u. a. (2011). Quantitative analysis of culture using millions of digitized books. Science, 331(6014), S. 176-182.

◐ Pechenick, E. A., Danforth, C. M. und Dodds, P. S. (2015). Characterizing the Google Books corpus. PLOS ONE, 10(10), e0137041.

● Bayerische Staatsbibliothek. Reichstagsprotokolle, Verhandlungen des Deutschen Reichstags 1867-1942. https://www.reichstagsprotokolle.de/

● Bibliothèque nationale de France. Gallica. https://gallica.bnf.fr/

● Deutsches Textarchiv (BBAW). https://www.deutschestextarchiv.de/

● Gale. The Times Digital Archive. https://www.gale.com/c/the-times-digital-archive

● Institut National de la Propriété Industrielle. Archives historiques. https://www.inpi.fr/en/archives-historiques-INPI

● Staatsbibliothek zu Berlin. ZEFYS. https://zefys.staatsbibliothek-berlin.de/

● UK Parliament. Historic Hansard, Volumes Index. https://api.parliament.uk/historic-hansard/volumes/index.html

*Gesichert aus einem Arbeits-Chat vom 20.11.2026; der Inhalt wurde im selben Chat in acht /check-Runden bis zur Stabilität geprüft (Fassung v7), nicht nur still. Flags: ● belegt, ◐ erwähnt, ○ ungeprüft.*
