# Dyadischer Anti-Catch-up-Presseindex, Fundierung Scaffold und Beschaffungsliste

*Aus einer rohen Projektidee wurde ein Deep-Research-Prompt gebaut, in zwei Läufen bearbeitet, beide Läufe geprüft und am Ende die Liste der noch zu beschaffenden Archive erstellt.*

## Kernpunkte
1. Gegenstand ist ein presse-basierter Index, der die Abwehr-Rhetorik etablierter Volkswirtschaften gegen aufholende Länder über fünf Frames und mehrere Dyaden hinweg misst, von UK gegen Deutschland (1870-1914) bis USA, Deutschland und Frankreich gegen China (seit 1995).
2. Der Index ist baubar, aber nur als gestuftes Werkzeug: belastbar für UK gegen Deutschland, USA gegen Japan und USA gegen China, nur explorativ für Deutschland gegen China, Frankreich gegen China und die EU gegen Japan vor 1994, weil dort offene Volltext-Archive fehlen.
3. Die fünf Frames sind analytisch trennbar, empirisch aber nicht sauber getrennt (Sicherheit und Technologieaneignung überlappen, der systemisch-ideologische Frame ist für UK gegen Deutschland fast leer), und mehrere heutige Anker wie „forced technology transfer" oder „systemic rival" gab es in früheren Epochen sprachlich noch nicht.
4. Das technische Gerüst liegt als lauffähiges, mit Beispieldaten befülltes Scaffold vor (zehn Artefakte, drei Datenebenen, drei parallele EU-Gewichtungen), das mit Archivzugang direkt gefahren werden kann; die gezeigten Indexwerte sind Platzhalter, keine Messungen.
5. Die Quellenprüfung lief zweimal je Dokument: die Fundierung steht als geprüfte v1, das Scaffold ist nach zwei Runden stabil (v2); offen bleibt nur die Beschaffung der zugangsgesperrten Archive.

## Was dieser Chat gebaut hat
Am Anfang stand eine ausführliche, rohe Projektbeschreibung für einen rekonstruierbaren, dyadischen Langfrist-Index. Daraus wurde ein Deep-Research-Prompt in zwei Teilen gebaut (im Chat hergeleitet): Lauf eins legt die konzeptionelle und quellenkritische Grundlage, Lauf zwei liefert das technische Gerüst. Beide Läufe wurden anschließend mit der Prüf-Kette abgeklopft, jede URL und jeder tragende Zahlen- oder Datumsclaim gegen die Primärquelle. Ergebnis sind zwei Dateien, beide im Begleit-ZIP: die geprüfte Fundierung und das stabile Scaffold.

## Die fünf Frames und der Index
Der Index misst je Dyade (Incumbent gegen Target) und Jahr fünf Deutungsrahmen der Berichterstattung:

1. Sicherheit und strategische Bedrohung (nationale Sicherheit, strategische Abhängigkeit, Dual-Use, geopolitische Rivalität).
2. Unfairer Wettbewerb und Regelverstoß (Dumping, Subventionen, Staatskapitalismus, Währungsmanipulation, IP-Verletzung).
3. Systemisch-ideologischer Konflikt (Autoritarismus, staatliche Lenkung, systemischer Rivale, Werte-Konflikt).
4. Deindustrialisierung und Beschäftigungsbedrohung (Arbeitsplatzverluste, Fabrikschließungen, Verlust der technologischen Führung).
5. Technologieaneignung und Spionage (Technologiediebstahl, reverse engineering, erzwungener Technologietransfer, Industriespionage).

Gerechnet wird in drei Kennzahlen (im Chat hergeleitet):

```
FrameIntensity_f(i,j,t) = Mittel der Vorhersage-Wahrscheinlichkeit für Frame f über alle relevanten Artikel
SalienceIndex(i,j,t)   = Target-Artikel / alle Wirtschaftsartikel des Incumbent-Landes-Jahres
OverallIndex(i,j,t)    = Mittel der fünf FrameIntensity-Werte
EU_index(j,t)          = gewichtetes Mittel der Mitgliedsländer, parallel in drei Varianten:
                         nach Wortzahl, nach Artikelzahl, gleichgewichtet
```

Intensität (Ton) und Salienz (Menge) bleiben bewusst getrennte Spalten, damit ein Ausschlag nicht Mengen- mit Tonverschiebung verwechselt. Die Anker sind epochenspezifisch und werden gemappt, nicht übersetzt; „forced technology transfer" (USTR 2018) und „systemic rival" (EU 2019) sind für 1900 gesperrt.

## Was messbar ist und was nicht
Belastbar sind die Dyaden mit offenem oder lizenziertem Volltext in Dichte: UK gegen Deutschland über das Times Digital Archive (über 1,6 Mio Seiten, 70.000 Ausgaben, in 11,8 Mio Artikel zerlegt, Digitalisierung 2002-2003), USA gegen Japan und USA gegen China über ProQuest Historical Newspapers TDM (etwa 99,1 Mio XML-Dateien, 26 Titel, per-Artikel-OCR-Score), Frankreich über Gallica und RetroNews (Abdeckung effektiv bis etwa 1950). Nur explorativ bleiben Deutschland gegen China (deutsche Presse nach 1990 hinter Paywalls, kein Bulk-Zugang), Frankreich gegen China (RetroNews endet um 1950) und die EU gegen Japan vor 1994 (EP-Verbatim erst ab 1994 durchsuchbar, davor nur Amtsblatt-Annex als Scan). Die größte nicht behebbare Schwäche ist die Digitalisierungs-Auswahl: welche Zeitungen überliefert und digitalisiert sind, ist nicht zufällig, also taugt der Index für Verläufe innerhalb einer Dyade besser als für Niveauvergleiche zwischen Ländern.

## Was die Prüfung ergab
Die Fundierung wurde einmal geprüft und steht als v1; zwei Datums- und Zuschreibungsfehler wurden dabei korrigiert (Made in China 2025 ist ein Erlass des Staatsrats vom 19.05.2015, nicht „von Li Keqiang unterzeichnet"; die Zuschreibung des Denman-Zitats wurde auf die belegte Fundstelle zurückgeführt). Das Scaffold wurde zweimal geprüft und ist nach Runde zwei stabil: in Runde eins fielen eine unbelegte Produktnummer und eine zu starke Zuschreibung („one-sided free trade" ist die Kampfvokabel der Fair-Trade-Bewegung, nicht das offizielle Motto der Fair Trade League); beide Restpunkte (Bernaciak 2012, Erstdatum von „dumping") wurden in Runde zwei primärbelegt aufgelöst. Geprüft und bestätigt wurden unter anderem: die EU-Formel „systemic rival" aus JOIN(2019) 5 vom 12.03.2019, die Section-301-Daten (Einleitung 18.08.2017, Befund 22.03.2018), Verordnung (EWG) Nr. 3545/82 samt der 80,5-Prozent-Marke der japanischen Videorecorder, Verordnung (EWG) Nr. 1761/87, die Halbleiterzahlen (Japans Weltmarktanteil 28 auf 50 Prozent 1978-1987, US-DRAM-Anteil 70 auf 20 Prozent), Williams „Made in Germany" (1896) und der IBM-Hitachi-Fall 1982.

## Die Beschaffungsliste
Für den echten Lauf fehlen nur die zugangsgesperrten Archive und ein Buch (im Chat als /get ausgegeben): Krippendorff, Content Analysis (3. Aufl.) für die Reliabilitätsschwellen; das Times Digital Archive (Gale, Abo, TDM-XML); ProQuest Historical Newspapers TDM (Abo, Nutzung mit datenrückhaltenden Systemen untersagt); RetroNews der BnF (Abo für Volltext und Bulk, Gallica-Teil offen); die deutschen Kommerzarchive Spiegel, FAZ, Zeit und Handelsblatt (Paywall, kein Bulk, Lizenzanfrage); die japanischen Archive Asahi Kikuzo und Yomidas Rekishikan (Abo); die EP-Debatten vor 1994 als Amtsblatt-Annex-Scans über EUR-Lex; sowie ZEFYS der Staatsbibliothek zu Berlin zur direkten Prüfung von OCR-Abdeckung und Ausgabenzahl. Die kopierfertigen Suchstrings dazu stehen im Chat unter dem /get-Titel.

## Offen und unsicher
Offen ist allein die Beschaffung der oben genannten Archive; ohne sie bleiben die drei explorativen Dyaden Vorlage statt Messung. Inhaltlich steht nichts mehr zur Korrektur an, beide Dokumente sind geprüft. Vor einem echten Lauf prüfenswert, aber im Scaffold schon als Problem markiert: die Definition des Salienz-Nenners (was zählt als Wirtschaftsartikel), das Labeling-Protokoll samt Inter-Coder-Reliabilität und das Retraining-Intervall des Klassifikators über 150 Jahre. Einzelne Metadaten blieben in der Prüfung unbestätigt und sind in den Dateien als „nicht prüfbar" geflaggt (etwa die genaue OCR-Abdeckung von ZEFYS und die Artikelzahl von RetroNews).

## Quellen
● Bernaciak, M. (2012). Social Dumping: Political Catchphrase or Threat to Labour Standards? ETUI Working Paper 2012.06. Brüssel: ETUI. (ssrn.com/abstract=2208393)
◐ Autor, D. H., Dorn, D. und Hanson, G. H. (2016). The China Shock: Learning from Labor-Market Adjustment to Large Changes in Trade. Annual Review of Economics, 8, 205-240.
◐ Boydstun, A. E. und Gross, J. H. (2014). Policy Frames Codebook.
◐ Card, D., Boydstun, A. E., Gross, J. H., Resnik, P. und Smith, N. A. (2015). The Media Frames Corpus. ACL-IJCNLP, 438-444.
● Chronicling America (Library of Congress). Suchbestand 1756-1963; loc.gov-API ab 04.08.2025; Bulk-OCR mit SHA-256. (chroniclingamerica.loc.gov)
◐ Entman, R. M. (1993). Framing: Toward Clarification of a Fractured Paradigm. Journal of Communication, 43(4), 51-58.
● Europäische Kommission und HR-VP (2019). EU-China, A Strategic Outlook. JOIN(2019) 5 final, 12.03.2019.
● Fair Trade League (gegr. August 1881, Großbritannien). (en.wikipedia.org/wiki/Fair_Trade_League)
◐ Gamson, W. A. und Modigliani, A. (1989). Media Discourse and Public Opinion on Nuclear Power. American Journal of Sociology, 95(1).
◐ Gitlin, T. (1980). The Whole World Is Watching.
◐ Gururangan, S. et al. (2020). Don't Stop Pretraining: Adapt Language Models to Domains and Tasks. ACL 2020.
● Hobbs, A. (2013). The Deleterious Dominance of The Times in Nineteenth-Century Scholarship. Journal of Victorian Culture, 18(4), 472-497.
● Irwin, D. A. (1996). Trade Politics and the Semiconductor Industry. In A. O. Krueger (Hg.), The Political Economy of American Trade Policy. Chicago: University of Chicago Press (NBER WP 4745). (nber.org)
◐ Krippendorff, K. (2013). Content Analysis: An Introduction to Its Methodology. 3. Aufl. Thousand Oaks: SAGE.
● Merchandise Marks Act 1887 (50 und 51 Vict. c. 28), Großbritannien.
● MERICS zu „Made in China 2025" als „declaration of war on Germany" (Internationale Politik Quarterly, 2026).
● OED und Etymonline, Stichwort „dumping" (Substantiv erstmals 1874; ökonomischer Sinn „by 1868"). (oed.com; etymonline.com)
● ProQuest Historical Newspapers, TDM-Collection (NYU Libraries TDM-Guide). (guides.nyu.edu/tdm/proquest-historical-newspapers)
● Rat der EG (1982). Verordnung (EWG) Nr. 3545/82 vom 21.12.1982, Überwachung der Einfuhren von Videorecordern aus Japan. (EUR-Lex 31982R3545)
● Rat der EG (1987). Verordnung (EWG) Nr. 1761/87 vom 22.06.1987, Änderung der VO (EWG) Nr. 2176/84 (Anti-Umgehung). (EUR-Lex 31987R1761)
● Staatsrat der VR China (2015). Made in China 2025, erlassen am 19.05.2015 (Notiz datiert 08.05.2015).
● The Times Digital Archive (Gale), Kennzahlen über den Oceanic-Exchanges-Datenreport. (oceanicexchanges.org)
● US Trade Representative (2018). Section 301 Findings, 22.03.2018 (Einleitung 18.08.2017, 82 FR 40213).
◐ van Aggelen, A. et al. (2017). The debates of the European Parliament as Linked Open Data. Semantic Web Journal.
◐ van Strien, D. et al. (2020). Assessing the Impact of OCR Quality on Downstream NLP Tasks. (DHN 2020)
● Viner, J. (1923). Dumping: A Problem in International Trade. Chicago: University of Chicago Press.
● WIPO. Pariser Verbandsübereinkunft, Artikel 10bis (Brüsseler Revision vom 14.12.1900, nicht im Originaltext 1883). (wipo.int)
● Williams, E. E. (1896). Made in Germany. London: Heinemann.
◐ Denman-Memo 1979 („workaholics living in rabbit hutches"), belegt über Hansard 1989 und JIIA; die im ersten Entwurf genannten Sekundärzuschreibungen wurden nicht bestätigt und entfernt.
◐ IBM-Hitachi-Fall 1982 (FBI-Sting), über FAS/Congress, UPI und Washington Post.
◐ Globalex und Georgetown-Law-EU-Guides (EP-Verbatim ab 1994 durchsuchbar, davor Amtsblatt-Annex).

*Gesichert aus einem Arbeits-Chat vom 20.11.2026, still geprüft, nicht mit /check auditiert. Flags: ● belegt, ◐ erwähnt, ○ ungeprüft.*
