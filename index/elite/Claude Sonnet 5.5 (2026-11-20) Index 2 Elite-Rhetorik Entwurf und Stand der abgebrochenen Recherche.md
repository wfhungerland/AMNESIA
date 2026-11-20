# Index 2 Elite-Rhetorik Entwurf und Stand der abgebrochenen Recherche

*Der Chat legte den Entwurf eines rekonstruierbaren, dyadischen Index für anti-aufholende Elitenrhetorik in Parlamenten und Regierungen fest, und der erste Recherchelauf dazu lieferte nach über einer Stunde kein verwertbares Ergebnis.*

## Kernpunkte
1. Index 2 misst, wie Parlamente und Exekutiven in Altländern (Incumbents) Aufholländer in fünf Frames beschreiben, und ist über Sprechakt, Institution und Land-Jahr-Dyade hinweg rückverfolgbar (im Chat vorgegeben).
2. Die Prioritätsreihenfolge bei unvollständiger Abdeckung ist: USA→China 1995-heute, USA→Japan 1965-1995, EU→China 1995-heute, UK→Deutschland 1870-1914 (von Fabian im Chat festgelegt).
3. Gelabelt wird zweistufig: LLM-Vorannotation mit festem Prompt, dann menschliche Validierung mit Intercoder-Maßen; trainiert wird nur auf validierten Labels (von Fabian im Chat festgelegt).
4. Der gestartete Recherchelauf zum Gesamtentwurf blieb ohne Inhalt (Ergebnistext nur „continued“, keine Quellen) und gilt als gescheitert.
5. Vorgeschlagen ist, den Auftrag in vier Teilläufe zu zerlegen; das ist noch nicht freigegeben.

## Ziel und Aufbau des Index
Der Index erfasst strategisch-politische Rede von Entscheidungsträgern gegenüber Aufholökonomien: Problemrahmung, Verantwortungszuschreibung, Handlungsaufforderung, normative Positionierung und historische Selbstverortung. Er ist vom Presseindex (Index 1) getrennt, teilt mit ihm aber das Frame-Wörterbuch `frame_dictionary.csv` (im Chat vorgegeben).

Jede Beobachtung muss auf eine konkrete Rede, einen Sprecher mit Rolle, Datum, Kammer und eine Dyade (Incumbent→Target) zurückführbar sein. Zwischenschritte werden gespeichert, es gibt keine undurchsichtige Aggregation.

Drei verschachtelte Ebenen:

1. Redesegment: speech_id, Sprecher, Partei, Rolle, Institution, Dyade, Datum, Volltext oder Kennung, Wortzahl, fünf Frame-Wahrscheinlichkeiten, fünf Ankerhäufigkeiten, Policy-Intent-Flag.
2. Institution-Jahr: Zahl der Reden, Wortzahl, mittlere Frame-Wahrscheinlichkeiten, mittlerer Policy-Intent-Wert.
3. Land-Jahr-Dyade: fünf Frame-Intensitäten, Gesamtindex, Policy-Intent-Index, Zahl der Reden, Wortzahl.

Die Dyaden in Prioritätsreihenfolge: USA→China (1995-heute), USA→Japan (1965-1995), EU→China (1995-heute), UK→Deutschland (1870-1914). Weitere im Auftrag genannte: EG/EU→Japan (1970-1995), Deutschland→China (1995-heute), Frankreich→Japan und/oder China (nach 1970). Für Europa entstehen nationale Indizes und ein EU-Institutionenindex, die Institutionenkennung bleibt erhalten.

## Die fünf Frames
1. Sicherheit und strategische Bedrohung.
2. Unfairer Wettbewerb und Regelverstoß.
3. Systemischer oder ideologischer Konflikt.
4. Deindustrialisierung und Beschäftigungsbedrohung.
5. Technologieaneignung und Spionage.

Daneben steht eine getrennte Policy-Intent-Ebene mit Begriffen wie „must impose“, „should restrict“, „introduce tariffs“, „export controls“, „legislation“, „ban“, „limit“, „screen“.

## Messung und Formeln
Die Messung ist ein Hybrid aus Ankerlexikon (Häufigkeit je Frame, normiert auf 1.000 Wörter) und überwachtem Klassifikator auf einer geschichteten, gelabelten Stichprobe je Dyade. Gespeichert werden Modelltyp, Split, Hyperparameter, Gütemaße und das serialisierte Modell.

| Größe | Definition |
|---|---|
| FrameIntensity_f(i,j,t) | Mittel der vorhergesagten Wahrscheinlichkeit von Frame f über alle Reden im Jahr t |
| OverallRhetoricIndex(i,j,t) | Mittel der FrameIntensity über die fünf Frames |
| PolicyIntentIndex(i,j,t) | Mittel des policy_intent_score über alle Reden |
| Salience(i,j,t) | Reden über das Zielland geteilt durch alle Wirtschaftsreden des Jahres |
| EU_index(j,t) | gewichtetes Mittel der Mitgliedstaaten- und EU-Institutionenindizes, Gewicht Redenzahl oder Wortzahl, beide Fassungen werden geliefert |

Alle Größen werden roh und konditional auf die Salienz des Ziellands ausgewiesen.

## Stichprobe und Vorverarbeitung
Je Incumbent i, Target j und Jahr t werden alle Redesegmente mit ausdrücklichem Bezug auf j gezogen, dann per fester Stichwortliste auf Wirtschafts-, Handels-, Industrie-, Technologie-, Sicherheits- und Außenwirtschaftskontexte eingeschränkt. Rein zeremonielle oder diplomatische Äußerungen entfallen. Alle Suchbegriffe und Protokolle werden gespeichert. Die Vorverarbeitung (OCR-Korrektur für frühe Perioden, Schreibvarianten, Lemmatisierung, Tokenisierung, Sprechermetadaten) ist skriptiert und reproduzierbar.

Quellen sind nur offizielle, öffentlich zugängliche, digitalisierte Archive mit dauerhaften Kennungen: Hansard (UK), Congressional Record (USA), Bundestag-Plenarprotokolle, Assemblée nationale und Sénat, Europäisches Parlament und Kommissionsmitteilungen. Die Institutionenabdeckung wird vorab in `institution_registry.csv` festgelegt, Brüche werden dokumentiert.

## Zweistufiger Annotationsworkflow
Stufe 1 ist eine LLM-Vorannotation mit festem Prompt, der direkt auf die Frame-Definitionen und Policy-Intent-Kriterien abbildet. Prompts, Modellversion, Temperatur und Rohausgaben werden gespeichert. Stufe 2 ist die menschliche Prüfung einer geschichteten Stichprobe mit gemessener Intercoder-Übereinstimmung und schriftlichem Adjudikationsprotokoll. Korrekturen fließen in den Trainingssatz zurück. Kein Zero-Shot-Ergebnis geht ohne menschliche Validierung in den Enddatensatz. Der Klassifikator wird nur auf validierten Labels trainiert, Vor- und Nachvalidierungslabels bleiben zur Prüfbarkeit erhalten (von Fabian im Chat festgelegt).

## Geforderte Ausgabedateien
Pflicht sind `institution_registry.csv`, `frame_dictionary.csv`, `labeled_speeches.csv`, `elite_speeches_panel.csv`, `elite_rhetoric_index.csv`, vollständige Replikationsskripte und eine Methodendokumentation. Zur Validierung dient `validation_report_elite.csv` (Jahr, Incumbent, Target, Flag bekannter Politikereignisse, Indexwerte), abgeglichen etwa mit den US-Halbleiterstreitigkeiten mit Japan, den WTO-Beitrittsdebatten zu China und den 5G-Debatten. Im Chat entstand keine dieser Dateien.

## Stand der Recherche
Nach Klärung von Ausgabeumfang, Annotationsstrategie und Dyadenpriorität wurde ein umfangreicher Recherchelauf mit elf Abschnitten (A bis K) gestartet: Methodik, Archivaudit, CSV-Schemata, Python-Gerüst, Frame-Lexika, Annotationsworkflow, EU-Behandlung, historische Anpassung, Salienz, Vergleichbarkeit mit Index 1, Validierungsanker. Der Lauf lief über eine Stunde und lieferte nur den Platzhalter „continued“ ohne Quellen.

Als Ursache wurde im Chat vermutet, dass der Auftrag für einen einzelnen Lauf zu lang und zu breit war (im Chat hergeleitet, nicht geprüft). Vorgeschlagen ist eine Aufteilung in vier Läufe:

1. Archivaudit, EU-Behandlung, historische Anpassung (Abschnitte B, G, H).
2. Frame-Wörterbuch, Annotationsworkflow, CSV-Schemata (C, E, F).
3. Replikationscode (D).
4. Validierungsanker, Salienz, Vergleichbarkeit mit Index 1 (I, J, K).

## Offen und unsicher
Offen ist, ob die Aufteilung in vier Läufe gewollt ist; die Frage an Fabian blieb unbeantwortet. Ungeprüft ist, ob der erste Lauf tatsächlich abgebrochen ist oder nur kein Ergebnis übergab. Die genannten Validierungsereignisse stammen aus dem Auftragstext und wurden im Chat nicht belegt. Nichts davon wurde vor dem Einsatz geprüft.

## Quellen
Im Chat trat keine Literatur auf, es wurden keine Quellen geliefert.

*Gesichert aus einem Arbeits-Chat vom 20.11.2026, still geprüft, nicht mit /check auditiert. Flags: ● belegt, ◐ erwähnt, ○ ungeprüft.*
