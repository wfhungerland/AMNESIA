# Displacement Before Escalation: Inventur und Kickstart

Stand 20.11.2026, ergänzt um den Policy Amnesia Index.

## Inventur

### A. Manuskript und Projektstand
| Stück | Stand | Wo |
|---|---|---|
| Manuskript (.tex), refs.bib, PDF | **fehlt**; weder auf C: noch in Dropbox; vermutlich nur in einem claude.ai-Projekt (etwa „OFFENE RECHERCHEN“ oder „SONDERWEG“) | claude.ai |
| Datensätze DS1 bis DS5 | **fehlen** als Dateien; nur in der Übergabenotiz beschrieben | claude.ai |
| Übergabenotiz „Project Handover State“ (01.08.2026): drei Thesen, Tabelle DS1 bis DS5 mit Lücken, Anhang E leer | da | Dropbox, Bibliothek/KI-Recherchen |
| „Manuscript Build and Repositioning Yield“ (26.08.2026): LaTeX-Fassung, Ausrichtung auf World Development, 38 Referenzen | da | dto. |
| „Literature Positioning Across Five Fields“ (03.08.2026), .md und .xlsx | da | dto. |
| „Systematic Literature Integration Across Five Fields“ (21.02.2026), frühe Fassung | da | dto. |
| „Germany Shock Paper Framing Options and Verified Empirical Spine“ (01.08.2026) | da | dto. |
| „Developmental State Institutional Persistence and Technology Transfer for World Development“ (27.07.2026), .md, .xlsx, Handover | da | dto. |

### B. Fallmaterial zu den vier Aufholfällen (Deutschland, Japan, Korea, China)
| Stück | Stand | Wo |
|---|---|---|
| „Incumbent Rhetoric and Policy Escalation After Technological Catch-Up in Four Cases“ (01.08.2026), .md und .xlsx; frühe Fassung vom 21.02.2026 | da | Dropbox, KI-Recherchen |
| „Imitation to Innovation: Technology Acquisition in Four Catch-Up Economies“, verifiziert v6 (sieben Prüfrunden, stabil) | da | ZIP vom 20.11. |
| „Technologischer Aufholprozess Deutschland, Japan, Korea und China“, verifiziert v3 (fünf Prüfrunden; 70-Prozent-Plateau der TFP, Technologieleistungsbilanz) | da | ZIP vom 20.11. |
| Koreanische und japanische Forschung zur deutschen Wirtschaftsgeschichte 1990 bis 2025 (Literaturüberblick, Teile ungeprüft) | da | Sicherung vom 20.11. |

### C. Messung der Rhetorik (Index 1 Presse, Index 2 Eliten)
| Stück | Stand | Wo |
|---|---|---|
| Index 1, „Anti-Catch-up Rhetoric Incumbent Press Dyadic Index Foundations“, verifiziert v1 | geprüft | ZIP vom 20.11. |
| Index 1, „Technical Scaffold“, verifiziert v2: lauffähiges Gerüst mit Beispieldaten, drei Datenebenen, drei EU-Gewichtungen; Werte sind Platzhalter | stabil | ZIP vom 20.11. |
| „Historical Press Language Five Frames Three Dyads“, verifiziert v5, dazu /bib-Kurzfassungen von Kennedy (1980) und Searle (1971) | stabil; zwei Saturday-Review-Stellen offen | ZIP vom 20.11. |
| „Digitised Primary Sources for Trade Competition Rhetoric Mapping 1850-1914“, verifiziert v7 (42 Quellen, acht Prüfrunden) | stabil | ZIP vom 20.11. |
| Policy Amnesia Index, Referenzarchitektur v2.5 (sieben Prüfrunden, stabil): misst, wie wenig die Etablierten an ihre eigene frühere Schutz- und Industriepolitik erinnern (Amnesie-Score aus der Rate historischer Selbstbezüge), sechs Dyaden 1870 bis heute; dazu Audit-Historie und Beschaffungsliste | stabil, drei Einzelangaben offen | ZIP vom 20.11. |
| Index 2, Elite-Rhetorik (Parlamente, Regierungen): Entwurf, Prioritäten der Dyaden, zweistufige Annotation festgelegt; Recherchelauf gescheitert; Aufteilung in vier Läufe vorgeschlagen, nicht freigegeben | Entwurf | Sicherung vom 20.11. |

### D. Offen
1. Manuskript, refs.bib und DS1 bis DS5 aus claude.ai sichern. Ohne sie kein Weiterschreiben.
2. Anhang E (Salienz der Absorptionsphase) bauen. Der Salienz-Teil von Index 1 (Artikel über das Zielland je Wirtschaftsartikel) passt genau dazu und kann Anhang E als einfache, belegte Messung tragen, ohne dass der ganze Index fertig sein muss.
3. Zwei Section-301-Fälle in einer Fußnote klären.
4. TFP Chinas aus Penn World Table 11 und Total Economy Database ergänzen; das Material „70-Prozent-Plateau“ liefert dafür schon geprüfte Werte.
5. Alle Zahlen des Manuskripts einmal prüfen.
6. Beschaffung: Saturday Review 1895 und 1897 (Bände 80, 84), Krippendorff (2013), Archive mit Abo (Times Digital Archive, ProQuest Historical Newspapers, RetroNews, HeinOnline), Buchzahlen (Johnson 1982, Kohli 2004, Odagiri und Goto 1993, Landes 1969, Broadberry 1998).
7. Entscheiden, ob Index 1, Index 2 und der Policy Amnesia Index (in seiner Architektur als Teil eines Oberprojekts mit Indizes 1 bis 3 beschrieben; welcher Index 3 ist, klären) eigene Projekte werden (Ziel: eigenes Paper oder Datensatz) und das Paper nur den kleinen Salienz-Baustein nutzt.

## Wo anfangen

1. **Zuerst in Claude (claude.ai oder Desktop-App), kurz:** nur um Manuskript, refs.bib und DS1 bis DS5 aus den claude.ai-Projekten zu holen. Claude Code kommt an diese Projekte nicht heran. Suchprompt dafür unten.
2. **Dann alles in Claude Code** mit dem Kickstart unten: Repo, Dateien, Rechnungen, LaTeX, Prüfung.

### Suchprompt für claude.ai (in jedem Projekt, das in Frage kommt, einmal einfügen)
```
Suche in den Chats dieses Projekts nach dem Manuskript „Displacement Before Escalation“ (vier Aufholfälle: Deutschland 1840 bis 1914, Japan 1950 bis 1990, Korea 1960 bis 1997, China 1978 bis 2024; Zielzeitschrift World Development). Gesucht sind die LaTeX-Datei, refs.bib und die Datensätze DS1 bis DS5, vor allem aus dem Chat um den 26.08.2026 („Manuscript Build and Repositioning Yield“). Nenne mir den Chat und gib mir jede gefundene Datei vollständig als Download aus. Nichts kürzen, nichts neu schreiben.
```

## Kickstart für Claude Code

```
Vorhaben: Paper „Displacement Before Escalation“ zur Einreichung bei World Development. Vier Fälle technologischen Aufholens: Deutschland 1840 bis 1914, Japan 1950 bis 1990, Korea 1960 bis 1997, China 1978 bis 2024. These: Erst verdrängt der Aufsteiger die Etablierten von ihren Märkten, danach eskaliert der politische Konflikt. Laut Projektlandkarte vom 11.11.2026 ist es inhaltlich fertig und in LaTeX gesetzt; einzige Sperre ist der leere Anhang E (Salienz der Absorptionsphase).

Arbeitsweise: Deutsch im Chat, kurz und in einfacher Sprache; das Paper auf Englisch. Erst kurzer Plan zur Freigabe, offene Entscheidungen als antippbare Fragen. Jede Zahl und jede Quelle am Original prüfen, nichts erfinden. Ich habe wenig Erfahrung mit Git: Schritte für mich einzeln, ein Befehl je Codeblock.

Repo: neues privates Repo hungerland-macro/displacement ohne Workflows (dann ohne Zusatzkosten), verknüpft mit dem Ideenpool im Makrowolf (hungerland-macro/macro, docs/ideen.md, Rubrik „Forschungsprojekte vollständig“, Block 8.9). Ordner: manuscript/, data/ (DS1 bis DS5), research/ (Notizen und geprüfte Recherchen), index/ (Rhetorik-Messung), procurement/ (Beschaffung).

Material, das ich hochlade oder das in Dropbox liegt (Bibliothek/KI-Recherchen):
- Manuskript, refs.bib, DS1 bis DS5 (aus claude.ai gesichert; falls noch nicht da, sofort sagen und warten)
- Übergabe „Project Handover State“ (01.08.2026), „Manuscript Build and Repositioning Yield“ (26.08.2026), Literatureinordnung in fünf Feldern, Rahmung des Falls Deutschland, Entwicklungsstaat-Literatur, Rhetorik und Politik in vier Fällen
- geprüfte Recherchen: Technology Acquisition in Four Catch-Up Economies (v6), Technologischer Aufholprozess mit 70-Prozent-Plateau (v3), Historical Press Language Five Frames Three Dyads (v5) samt Kennedy (1980) und Searle (1971), Digitised Primary Sources 1850-1914 (v7), Anti-Catch-up Press Index Foundations (v1) und Technical Scaffold (v2), Entwurf Index 2 Elite-Rhetorik, Policy Amnesia Index (Referenzarchitektur v2.5 mit Audit-Historie und Beschaffungsliste), koreanische und japanische Forschung zur deutschen Wirtschaftsgeschichte

Schritte:
1. Inventur im Repo: alles ablegen, eine Übersicht README.md mit Stand je Datei; prüfen, ob Manuskript und DS1 bis DS5 zusammenpassen (Zahlen im Text gegen Daten).
2. Anhang E: Vorschlag, wie die Salienz der Absorptionsphase je Fall gemessen wird, möglichst mit dem Salienz-Baustein des Presseindex (Artikel über das Zielland je Wirtschaftsartikel) aus frei zugänglichen Quellen (Chronicling America, Hansard, Reichstagsprotokolle, Gallica); was nur mit Abo-Archiven geht, als Beschaffung markieren. Erst Vorschlag, dann rechnen.
3. Fußnote zu zwei Section-301-Fällen; TFP Chinas (Penn World Table 11, Total Economy Database), abgeglichen mit dem Material zum 70-Prozent-Plateau.
4. Ganzes Manuskript einmal prüfen (Tabelle: Aussage, Quelle, geprüft ja oder nein), LaTeX kompilieren.
5. Autorenhinweise von World Development, Anschreiben, Vorschläge für Gutachter. Nicht einreichen; das mache ich selbst.
Getrennt halten: Index 1, Index 2 und den Policy Amnesia Index als eigene, größere Vorhaben; hier nur, was Anhang E braucht. Das zweite Manuskript zu Deutschland und Vietnam gehört nicht in dieses Repo.
```
