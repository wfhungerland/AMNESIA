# manuscript

Manuskript „Displacement Before Escalation“ (World Development), Fassung vom 22.11.2026. Nicht einreichen.

| Datei | Inhalt |
|---|---|
| `main.tex`, `main.pdf` | Manuskript (elsarticle, review); bauen mit `latexmk -pdf main.tex` |
| `refs.bib` | Literatur; Prüfvermerke stehen als Kommentare über den Einträgen, nicht im gedruckten Verzeichnis |
| `online_appendix.md`, `online_appendix.pdf` | Online-Anhang A bis L (früher Anhang E); bauen mit `python3 manuscript/build_appendix.py` (pandoc, pdflatex; fügt die Reaktionstabellen aus `data/ds1_events.csv` ein) |
| `claims_check.csv` | jede Zahl des Textes mit Quelle und Prüfstand; Spalte `section` nennt Abschnitte des Haupttexts (Ziffern) und des Anhangs (Buchstaben) |
| `outline.md` | Gliederung mit Kernaussage je Abschnitt |
| `figures/` | Abbildungen und ihre Skripte (`fig_main.py`: Abbildung 1 und K1; `fig_e1.py`: E1; `fig_e2_crec.py`: I1) |

Die alte Fassung vom 26.08.2026 ist verloren; Neubau nach den Daten.
