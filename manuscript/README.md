# manuscript

Manuskript „Trade Policy Amnesia: How Far Leading Economies Go Against Late Industrialisers, 1850-2024“ (World Development; früher „Displacement Before Escalation“), Fassung vom 25.11.2026. Nicht einreichen.

| Datei | Inhalt |
|---|---|
| `main.tex`, `main.pdf` | Manuskript (elsarticle, review); bauen mit `latexmk -pdf main.tex` |
| `titlepage.tex`, `titlepage.pdf` | getrennte Titelseite für die doppelt anonymisierte Begutachtung (Autor, Adresse, Danksagung, Interessenkonflikte, Finanzierung, CRediT); Platzhalter in eckigen Klammern ausfüllen |
| `refs.bib` | Literatur; Prüfvermerke stehen als Kommentare über den Einträgen, nicht im gedruckten Verzeichnis |
| `online_appendix.md`, `online_appendix.pdf` | Online-Anhang A bis L (früher Anhang E); bauen mit `python3 manuscript/build_appendix.py` (pandoc, pdflatex; fügt die Reaktionstabellen aus `data/ds1_events.csv` ein) |
| `highlights.txt` | Highlights (5 Zeilen, je höchstens 85 Zeichen mit Leerzeichen; Elsevier-Standard, laut Guide for Authors für Regular Papers nicht verlangt) |
| `claims_check.csv` | jede Zahl des Textes mit Quelle und Prüfstand; Spalte `section` nennt Abschnitte des Haupttexts (Ziffern) und des Anhangs (Buchstaben) |
| `outline.md` | Gliederung mit Kernaussage je Abschnitt |
| `Figure_1.pdf` bis `Figure_6.pdf` | Abbildungen als eigene Dateien für die Einreichung, in der Reihenfolge des Texts |
| `figures/` | Abbildungen und ihre Skripte (`style.py`: gemeinsamer Stil; `fig_story.py`: Abbildungen 1 bis 6 und L.1; `fig_e1.py`: E.1; `fig_e2_crec.py`: G.1) |

Die alte Fassung vom 26.08.2026 ist verloren; Neubau nach den Daten.

## Vor der Einreichung offen (Stand 25.11.2026, gegen Guide for Authors geprüft)

- Titelseite: ausgefüllt am 25.11.2026; Art der Hilfe in der Danksagung bei Bedarf präzisieren.
- KI-Erklärung: Entwurf im Manuskript; vor der Einreichung auf Vollständigkeit prüfen.
- Daten: Paket mit `python3 replication/build_package.py` bauen (`dist/replication_package.zip`, anonymisiert), hochladen, anonymen Link in „Data availability“ eintragen.
- Zweitcodierung (Krippendorffs Alpha) nachtragen.
- Hochladen: `main.tex`, `refs.bib`, `main.bbl`, `Figure_1.pdf`, `titlepage` getrennt, `online_appendix.pdf` als Supplementary Material.
