# data

DS1 bis DS5 und die Prüfungen für „Displacement Before Escalation“. Neubau vom 20. bis 22.11.2026. Alle fünf Datensätze und der Online-Anhang (manuscript/online_appendix.md, früher Anhang E) stehen; offen ist die Zweitcodierung von DS1.

Reproduzieren aus dem Repo-Wurzelordner:

```bash
bash data/fetch.sh
```

```bash
python3 data/build.py
```

Danach alle Auswertungen mit `bash data/run_all.sh` oder einzeln in dieser Reihenfolge (Hansard-Skripte laufen lange). API-Schlüssel als Umgebungsvariablen `COMTRADE_KEY` und `GOVINFO_KEY`.

```bash
python3 data/hansard_salience.py && python3 data/hansard_competition.py && python3 data/hansard_sectors.py && python3 data/hansard_usa.py && python3 data/hansard_phrases.py
```

```bash
python3 data/third_markets.py && python3 data/comtrade_milestones.py && python3 data/registers_ttbd.py && python3 data/registers_product_displacement.py
```

```bash
python3 data/tests_sequence.py && python3 data/tests_cycle.py && python3 data/population_test.py && python3 data/population_panel.py && python3 data/population_employment.py
```

Rohdaten liegen in `data/raw/` und sind nicht eingecheckt. Ihre Prüfsummen vom Abruf am 20.11.2026 stehen in `data/raw/SHA256SUMS.abruf`. Keine Interpolation, keine Glättung.

## Quellenkarte

| ID | Datei | Inhalt | Quelle | Abdeckung | Lizenz |
|---|---|---|---|---|---|
| DS1 | `ds1_milestones.csv`, `ds1_responses.csv` → `ds1_events.csv` | 18 Verdrängungsmeilensteine, 41 Reaktionen der Etablierten, Punkte IR 1–5 (Regel: `ds1_reach_rubric.md`), Phase und Lag | Material im Repo, für Japan 1950–1980 Webrecherche vom 21.11.2026 | Entwurf, Zweitcodierung offen | – |
| DS1-H | `ds1_hansard_salience.csv`, `ds1_hansard_sections.csv` | Nennung Deutschlands in britischen Wirtschaftsdebatten 1850–1914: Anteil der Debatten, Treffer je 100.000 Wörter, Anteil mit Wettbewerbswort im Umkreis von 30 Wörtern | Historic Hansard (api.parliament.uk), 281.577 Debatten, davon 15.126 Wirtschaftsdebatten per Titelfilter `econ_v2`; Skripte `hansard_salience.py`, `hansard_competition.py` | 1850–1914; 1850–1856 unter 900 Debatten je Jahr | Open Parliament Licence |
| Drittmärkte | `third_markets_tradhist.csv`, `third_markets_summary.csv` | Ausfuhren von USA und Deutschland in Drittmärkte relativ zu Großbritannien, fester Kreis von 17 Märkten | CEPII TRADHIST v4 (Fouquin und Hugot 2016); Skript `third_markets.py` | 1871–1913 | CEPII-Nutzungsbedingungen, nicht geprüft |
| DS2 | `ds2_gdppc.csv` | BIP pro Kopf (2011-PPP-Dollar), Verhältnis zu USA und GBR | Maddison Project Database 2023 (Bolt und van Zanden 2024), doi:10.34894/INZBF2 | bis 2022; jährlich lückenlos: DEU ab 1500, JPN ab 1885, KOR ab 1946, CHN ab 1950 | CC BY 4.0 |
| DS3 | `ds3_tfp.csv` | TFP-Niveau relativ zu den USA (`ctfp`, USA = 1 je Jahr); zusätzlich `rtfpna` (eigene Entwicklung, 2017 = 1) | Penn World Table 11.0 (Feenstra, Inklaar und Timmer 2015; Version 11.0, 2025), doi:10.34894/FABVLR | DEU, JPN 1954–2023; CHN 1956–2023; KOR 1957–2023 | CC BY 4.0 |
| DS4 | `ds4_basic_research.csv` | Grundlagenforschung: Anteil an GERD, in % des BIP, Sektoren Staat + Hochschulen in % des BIP | OECD, GERD by sector of performance and type of R&D (DF_GERD_TORD); OECD MSTI, GERD in % des BIP | JPN, USA 1981–2024; CHN 1991–2024; KOR 1995–2024; **DEU fehlt** | OECD-Nutzungsbedingungen |
| DS5 | `ds5_tbp.csv` | Lizenzgebühren: Einnahmen, Zahlungen, Saldo, Deckungsgrad, Saldo in % des BIP | Weltbank WDI, BX.GSR.ROYL.CD, BM.GSR.ROYL.CD, NY.GDP.MKTP.CD (Stand 11.11.2026) | DEU 1971, KOR 1976, JPN 1996, CHN 1997, jeweils bis 2025 | CC BY 4.0 |

Spalten: `ratio_usa` = gdppc / gdppc USA; `br_share_gerd` = GERD Grundlagenforschung / GERD gesamt; `br_pct_gdp` = br_share_gerd × GERD in % BIP; `br_gov_hes_pct_gdp` = (Grundlagenforschung Staat + Hochschulen) / GERD gesamt × GERD in % BIP; `coverage_ratio` = Einnahmen / Zahlungen.

## Abgleich mit dem alten Projektstand

Gegenübergestellt sind die Angaben aus der Übergabe vom 01.08.2026 („Übergabe“), dem Germany-Shock-Papier und dem Bericht zum 70-Prozent-Plateau mit den neuen Daten. Abweichungen müssen ins neue Manuskript.

| Nr. | Alte Angabe | Neuer Wert | Urteil |
|---|---|---|---|
| 1 | Übergabe: DS3 aus PWT-Variable RTFPNA | RTFPNA misst TFP gegen das eigene Jahr 2017, nicht gegen die USA; der Ländervergleich braucht CTFP | Methodenfehler, korrigiert |
| 2 | Übergabe: PWT endet 2019, China ab 2020 aus der Total Economy Database | PWT 11.0 reicht für alle vier Fälle bis 2023 | Ergänzung entfällt |
| 3 | Übergabe: Japans TFP gipfelt um 1991 bei rund 0,68 | 0,796 im Jahr 1991 | falsch |
| 4 | Übergabe: Japan heute rund 0,64 | 0,640 (2023) | bestätigt |
| 5 | Übergabe: Korea seit 2010–2012 bei rund 0,66 | 0,621 bis 0,700 (2010–2023), 0,661 (2023); Höchstwert 0,711 (2002) | bestätigt |
| 6 | Übergabe: Deutschland bei oder über US-Parität | über 1 in 2000–2008 und 2017–2023, 0,95 bis 0,99 in 2010–2016; Höchstwert 1,046 (2002) | bestätigt mit Einschränkung |
| 7 | Germany Shock: deutsche TFP nur 85 bis 95 Prozent, nie klar über 100 | widerspricht PWT 11.0 (Nr. 6) | widerlegt |
| 8 | Übergabe: China bei rund 33 Prozent des US-BIP pro Kopf | 0,329 (2022) | bestätigt |
| 9 | Build-Notiz: TFP-Verlangsamung setzt bei 0,60 bis 0,73 ein | Japan stockt bei 0,78 bis 0,80 (1990–1991), Korea bei 0,69 bis 0,71 (2000–2010) | Spanne zu niedrig; Japan liegt außerhalb |
| 10 | 70-Prozent-Bericht: China 2023 bei 41 Prozent | 0,471 (2023); 0,41 war der Stand um 2015 | veraltet |
| 11 | 70-Prozent-Bericht: Korea 1990 bei rund 52, Deutschland 1970 bei rund 80 | 0,618 und 0,664 | falsch |
| 12 | Build-Notiz: Schwelle von 1,0 Prozent des BIP für Grundlagenforschung von Staat und Hochschulen, von keinem Land erreicht | Höchstwert USA 0,35 Prozent, Korea 0,30, Japan 0,23, China 0,17 | bestätigt; die Schwelle liegt so hoch, dass sie nichts trennt |
| 13 | Übergabe: Deutschland fehlt bei der Grundlagenforschung | OECD meldet für Deutschland Grundlagenforschung nur für Unternehmen und Staat ab 2006/2007, nicht für Hochschulen | bestätigt |
| 14 | Übergabe: DS5 deckt 1970–2023 | Weltbank: DEU ab 1971, KOR ab 1976, JPN erst ab 1996, CHN ab 1997 | Japans Aufholphase fehlt; Quelle Bank of Japan oder NISTEP nötig |
| 15 | 70-Prozent-Bericht: deutsche Bilanz kippt 2003 bis 2008 ins Plus | Weltbank: erster Überschuss 2009 | abweichend, Quelle klären (Bundesbank) |
| 16 | 70-Prozent-Bericht: Deutschland 1971 Einnahmen 156, Zahlungen 423 Mio. Dollar | 0,156 und 0,423 Mrd. Dollar, Deckungsgrad 0,37 | bestätigt |
| 17 | 70-Prozent-Bericht: China 2024 Zahlungen 45,8, Einnahmen rund 10,1, Saldo −35,7 Mrd. Dollar | Weltbank: 45,87, 7,07, −38,80 | Zahlungen bestätigt; Einnahmen und Saldo hängen an der Quelle (SAFE gegen Weltbank) |
| 18 | 70-Prozent-Bericht: Korea 2024 Saldo −3,85 Mrd. Dollar (MSIT) | Weltbank: −2,69 | andere Abgrenzung, beide angeben |

Weitere Auffälligkeit: Die Weltbank-Reihe für Korea zeigt 1976–1979 winzige Überschüsse auf sehr kleiner Basis. Das ist kein inhaltlicher Befund und gehört so markiert.

## Offen

- DS1: Zweitcodierung (`ds1_coder2_blank.csv`), danach Krippendorffs α.
- DS4 für Deutschland: Grundlagenforschung der Hochschulen aus Bundesbericht Forschung und Innovation oder Institutsbudgets (Max Planck, DFG).
- DS5 für Japan vor 1996: Bank of Japan, Zahlungsbilanz; NISTEP-Technologiehandel.

## Prüfungen

| Datei | Inhalt | Skript |
|---|---|---|
| `ds1_export_milestones.csv`, `ds1_export_series.csv` | Meilensteine nach der Exportregel (Gegenprobe) | `comtrade_milestones.py` |
| `third_markets_tradhist.csv`, `third_markets_summary.csv`, `tyszynski_1951_selected.csv` | Drittmärkte 1871–1913; Tyszynski (1951) Tabellen I, II, VIII | `third_markets.py` |
| `cotton_piece_goods_1913_1938.csv`, `tyszynski_1951_japan.csv` | Baumwollstoffe GB und Japan 1913–1938 (Robson 1957, Sandberg 1974); Tyszynski Tab. III und IV (1929, 1937) | abgeschrieben (Zahlenauszug der Bibliothek) |
| `third_markets_1930s.csv`, `third_markets_1930s_summary.csv` | Japan gegen Großbritannien: Drittmärkte 1920–1938 (TRADHIST) | `third_markets_1930s.py` |
| `ds1_hansard_japan.csv`, `ds1_hansard_japan_sections.csv` | Nennungen Japans in britischen Wirtschaftsdebatten 1920–1939 | `hansard_japan.py` |
| `conditionality.txt`, `conditionality_challengers.csv` | IWF-Auflagen nach Politikfeld 1989–2014, US-Hilfe 1980–2011, Sicherheitsrat und UN-Nähe (Stubbs et al. 2020, 2016) | `conditionality.py` |
| `geopolitics_instruments.csv`, `geopolitics_dyads.csv`, `geopolitics.txt`, `geo_instrument_mode.csv` | Bündnis (ATOP 5.1), UN-Abstand (Bailey/Strezhnev/Voeten), Machtverhältnis (COW CINC v7) je Instrument und Meilenstein; Art der Maßnahme | `geopolitics.py` |
| `cases_crossovers.csv`, `cases_breadth.csv`, `cases_hazard.csv`, `cases_register_tested.csv`, `cases_panel.csv`, `cases_panel.txt` | Weitere Fälle TH, VN, MY, MX, BR, HK, TW (mit JP, KR, CN zum Vergleich der Reichweite) | `cases_fetch.py`, `cases_test.py` |
| `ds1_hansard_sectors.csv`, `ds1_hansard_usa.csv`, `ds1_hansard_phrases.csv` | Hansard nach Sektor, Nennung der USA, Wendungen | `hansard_*.py` |
| `ds1_registers.csv`, `ds1_registers_summary.txt` | 759 AD/CVD-Verfahren von USA und EU gegen JP, KR, CN (TTBD, Bown) | `registers_ttbd.py` |
| `ds1_product_displacement.csv` | 127 US-AD-Fälle gegen China, Importanteil vor dem Fall | `registers_product_displacement.py` |
| `tests_sequence.txt`, `tests_cycle.txt`, `tests_cycle_events.csv` | Binomial- und Placebotest, Bruchtest; Konjunktur (HP-Filter) | `tests_sequence.py`, `tests_cycle.py` |

## Gutachten: Register, Population, Kontrollgruppe, Gewicht

Rohdaten dazu: Comtrade AG3/AG4 (`population_fetch*.py`), WITS-Konkordanzen HS–SITC, Census-Konkordanz der Einfuhrwaren 2002, NBER-CES (NAICS 1997). Alle über `fetch.sh`.

| Datei | Inhalt |
|---|---|
| `broad_register.csv` → `broad_register_tested.csv` | 23 breite US-Maßnahmen gegen JP, KR, CN (1957–2024), Phase gegen die Exportkreuzung |
| `population_crossovers.csv`, `population_hazard.csv` | verdrängte Warengruppen und Anteil mit breiter Maßnahme binnen 10 Jahren (`population_test.py`) |
| `population_panel.csv`, `population_panel.txt` | Panel Gruppe × Jahr, Kontrollgruppe, AD/CVD-Fälle (`population_panel.py`) |
| `population_weight.csv`, `population_employment.txt` | Gewicht: US-Einfuhren und US-Beschäftigung (NBER-CES) im Kreuzungsjahr (`population_employment.py`) |
