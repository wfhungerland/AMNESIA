# Replication package: Trade Policy Amnesia

This package reproduces the datasets, tests, tables and figures of the manuscript "Trade Policy Amnesia: When Leading Economies Turn Against Late Industrialisers, 1850-2024" and its online appendix.

## Contents

| Folder or file | Content |
|---|---|
| `data/*.csv`, `data/*.txt` | All derived datasets and test outputs used in the paper |
| `data/ds1_milestones.csv`, `data/ds1_responses.csv` | Hand-coded core data: 18 sectoral displacement milestones and 41 incumbent responses, each with its source and a check note |
| `data/broad_register.csv` | Register of 42 broad US instruments with legal basis and source |
| `data/ds1_reach_rubric.md` | Coding rule for the instrument-reach score (IR 1–5) |
| `data/ds1_coder2_blank.csv` | Blank sheet for the independent second coding |
| `data/*.py` | Retrieval and analysis scripts |
| `data/fetch.sh` | Downloads all third-party raw data into `data/raw/` |
| `data/run_all.sh` | Runs all analyses and figures in order |
| `data/raw/SHA256SUMS.abruf` | Checksums of the raw files as retrieved for the paper |
| `manuscript/figures/*.py` | Figure scripts (`style.py`: shared look; `fig_story.py`: Figs. 1-6 and L.1; `fig_e1.py`, `fig_e2_crec.py`: Figs. E.1 and G.1) |
| `manuscript/online_appendix.md`, `manuscript/build_appendix.py` | Source of the online appendix and its build script |
| `requirements.txt` | Python packages |

Check notes, column comments and some script comments are in German. Variable names and file names are in English or self-explanatory; `data/README.md` describes every file.

## Requirements

- Python 3.11 or later with the packages in `requirements.txt` (`pip install -r requirements.txt`).
- `bash`, `curl`, `unzip`, `sha256sum`.
- For the appendix PDF only: `pandoc` and a LaTeX installation with `pdflatex`.
- Several gigabytes of disk space for the raw data (TRADHIST alone is about 1.1 GB).
- Free API keys, set as environment variables before running `fetch.sh`:
  - `COMTRADE_KEY`: UN Comtrade (https://comtradedeveloper.un.org);
  - `GOVINFO_KEY`: api.data.gov key for govinfo (https://api.data.gov/signup).

## Steps

Run from the package root:

```bash
pip install -r requirements.txt
bash data/fetch.sh
bash data/run_all.sh
python3 manuscript/build_appendix.py
```

`fetch.sh` downloads the raw data and writes their checksums. Compare them with `data/raw/SHA256SUMS.abruf`; sources that publish revised vintages (for example UN Comtrade, World Bank WDI, OECD) can differ from the files used in the paper. The Historic Hansard and Congressional Record scripts download several hundred thousand pages on first run and take several hours; later runs use the local copies.

## Raw data and licences

Raw data are not included, because several licences do not allow redistribution. All sources are public:

| Source | Use | Licence |
|---|---|---|
| Penn World Table 11.0 (doi:10.34894/FABVLR) | TFP relative to the US | CC BY 4.0 |
| Maddison Project Database 2023 (doi:10.34894/INZBF2) | GDP per head | CC BY 4.0 |
| UN Comtrade | Exports and imports by product group | UN Comtrade terms of use |
| CEPII TRADHIST v4 | Bilateral trade | CEPII terms of use |
| Temporary Trade Barriers Database (World Bank) | AD, CVD and safeguard cases | CC BY 4.0 |
| World Bank WDI | Royalty payments and receipts, GDP | CC BY 4.0 |
| OECD MSTI and GERD by type of R&D | Basic research | OECD terms of use |
| NBER-CES Manufacturing Database; US Census concordance; WITS concordances | Employment and concordances | public |
| Historic Hansard (api.parliament.uk) | British parliamentary debates 1850–1939 | Open Parliament Licence |
| govinfo: Congressional Record, Federal Register | US congressional debates; notices | public domain |
| ATOP 5.1; COW National Material Capabilities v7; UN General Assembly ideal points (Bailey, Strezhnev and Voeten) | Alignment and power | as published by the providers |
| IMF conditionality and US aid data (Stubbs et al.) | Conditionality | as published on Harvard Dataverse |

The hand-coded data (milestones, responses, registers) and all derived files are the author's work. Licence: derived data CC BY 4.0, code MIT.

## Map from paper to files

| Paper | Files | Script |
|---|---|---|
| Tables 1 and 2, Fig. 1, Appendix B | `ds1_milestones.csv`, `ds1_export_milestones.csv`, `ds1_export_series.csv` | `build.py`, `comtrade_milestones.py`, `fig_story.py` |
| Table 3, Fig. 2, Appendix C | `ds1_events.csv`, `tests_sequence.txt`, `tests_cycle.txt`, `ds1_initiation.csv`, `tests_initiation.txt` | `build.py`, `tests_sequence.py`, `tests_cycle.py`, `tests_initiation.py`, `fig_story.py` |
| Table 4, Figs. 3 and 4, Appendix D | `ds1_registers.csv`, `population_*.csv`, `population_*.txt`, `broad_register_tested.csv`, `robust_broad.txt`, `robust_broad_es.csv` | `registers_ttbd.py`, `population_test.py`, `population_panel.py`, `population_employment.py`, `robust_broad.py` |
| Table 5 panel A, Fig. 5, Appendices E and F | `ds1_hansard_*.csv` | `hansard_*.py` |
| Table 5 panel B, Appendix G | `ds1_crec_*`, `ds1_crecb_*`, `ds1_kr_*`, `ds1_share_*` | `crec_*.py`, `crecb_*.py` |
| Appendix H | `cases_*.csv`, `cases_panel.txt`, `third_markets_1930s*.csv`, `cotton_piece_goods_1913_1938.csv` | `cases_test.py`, `third_markets_1930s.py`, `hansard_japan.py` |
| Appendix I | `geopolitics*.csv`, `geopolitics.txt`, `conditionality*.csv`, `conditionality.txt` | `geopolitics.py`, `conditionality.py` |
| Fig. 6, Appendix L | `ds2_gdppc.csv`, `ds3_tfp.csv`, `ds4_basic_research.csv`, `ds5_tbp.csv` | `build.py` |

`cotton_piece_goods_1913_1938.csv`, `tyszynski_1951_*.csv` and the hand-coded files are transcribed from printed sources; each row names its source and page.
