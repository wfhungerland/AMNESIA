# data

DS1 bis DS5 für „Displacement Before Escalation“. DS2 bis DS5 stehen (Neubau vom 20.11.2026), DS1 und Anhang E folgen nach Freigabe des Messvorschlags.

Reproduzieren aus dem Repo-Wurzelordner:

```bash
bash data/fetch.sh
```

```bash
python3 data/build.py
```

Rohdaten liegen in `data/raw/` und sind nicht eingecheckt. Ihre Prüfsummen vom Abruf am 20.11.2026 stehen in `data/raw/SHA256SUMS.abruf`. Keine Interpolation, keine Glättung.

## Quellenkarte

| ID | Datei | Inhalt | Quelle | Abdeckung | Lizenz |
|---|---|---|---|---|---|
| DS1 | `ds1_milestones.csv`, `ds1_responses.csv` → `ds1_events.csv` | 16 Verdrängungsmeilensteine, 39 Reaktionen der Etablierten, Punkte MSS 1–5 (Regel: `ds1_mss_rubric.md`), Phase und Lag | Material im Repo, für Japan 1950–1980 Webrecherche vom 21.11.2026 | Entwurf, Zweitcodierung offen | – |
| DS1-H | `ds1_hansard_salience.csv`, `ds1_hansard_sections.csv` | Nennung Deutschlands in britischen Wirtschaftsdebatten 1850–1914: Anteil der Debatten, Treffer je 100.000 Wörter, Anteil mit Wettbewerbswort im Umkreis von 30 Wörtern | Historic Hansard (api.parliament.uk), 281.577 Debatten, davon 15.126 Wirtschaftsdebatten per Titelfilter `econ_v2`; Skripte `hansard_salience.py`, `hansard_competition.py` | 1850–1914; 1850–1856 unter 900 Debatten je Jahr | Open Parliament Licence |
| Drittmärkte | `third_markets_tradhist.csv`, `third_markets_summary.csv` | Ausfuhren von USA und Deutschland in Drittmärkte relativ zu Großbritannien, fester Kreis von 17 Märkten | CEPII TRADHIST v4 (Fouquin und Hugot 2016); Skript `third_markets.py` | 1871–1913 | Etalab Open Licence |
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

- DS1 und Anhang E: Messvorschlag folgt.
- DS4 für Deutschland: Grundlagenforschung der Hochschulen aus Bundesbericht Forschung und Innovation oder Institutsbudgets (Max Planck, DFG).
- DS5 für Japan vor 1996: Bank of Japan, Zahlungsbilanz; NISTEP-Technologiehandel.
