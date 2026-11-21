# DS1: Punkteskala für Reaktionen der Etablierten (IR 1 bis 5)

IR steht für Instrument Reach, die Reichweite der Maßnahme. Die Skala hieß früher Manifest Salience Score (MSS); umbenannt nach dem Gutachten, weil sie Reichweite und Bindung misst, nicht Aufmerksamkeit. Sie misst, wie weit und wie bindend eine Reaktion des Etablierten den Aufsteiger trifft. Gezählt wird die Maßnahme selbst, nicht die Lautstärke der Debatte.

| Punkte | Stufe | Regel | Beispiel |
|---|---|---|---|
| 1 | Rede | öffentliche Äußerung ohne amtliches Verfahren | Williams (1896); Sullivan (2022) |
| 2 | Verfahren | amtliche Untersuchung, Anhörung, Beschwerde, Klage bei der WTO; noch nichts bindend | Royal Commission 1885; Section-301-Verfahren |
| 3 | enge Bindung | bindend, aber schmal: Kennzeichnung, Patentrecht, Antidumping auf ein Produkt, Pflichten für einzelne Rechte | Merchandise Marks Act 1887; Antidumping auf koreanische DRAM 1993 |
| 4 | Sektorbindung | bindende Mengen- oder Preisgrenze für einen ganzen Sektor, oder ein Handelsgesetz mit neuen Sanktionsrechten | Auto-Selbstbeschränkung 1981; Halbleiterabkommen 1986 |
| 5 | breite Bindung oder Verweigerung | Zölle auf große Teile der Einfuhr, oder Abschneiden von Technik für einen Sektor oder einen nationalen Champion | Section-301-Zölle 2018; Entity List Huawei 2019; Exportkontrollen Oktober 2022 |

Zweifelsfälle: Bei zwei möglichen Stufen gilt die niedrigere, mit kurzem Vermerk. Maßnahmen, die nur das eigene Land stärken (Bildungsgesetze, CHIPS Act), zählen nicht als Reaktion gegen den Aufsteiger und stehen nicht in DS1.

## Phase

- Jede Reaktion gehört zu einem Meilenstein (`ds1_milestones.csv`). Sektorbezogene Maßnahmen gehören zum Meilenstein ihres Sektors, Maßnahmen für die ganze Wirtschaft zum ersten Meilenstein des Falls.
- **absorption**: Reaktion vor dem Meilensteinjahr. **post**: im Meilensteinjahr oder danach. Lag = Reaktionsjahr minus Meilensteinjahr.

## Zweitcodierung

`ds1_coder2_blank.csv` enthält alle Reaktionen ohne meine Punkte. Trage in `reach_coder2` je eine Zahl von 1 bis 5 ein, ohne in `ds1_events.csv` nachzusehen. Danach rechne ich die Übereinstimmung (Krippendorffs Alpha, ordinal).
