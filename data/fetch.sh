#!/usr/bin/env bash
# Laedt die Rohdaten fuer DS2 bis DS5 nach data/raw/. Aufruf aus dem Repo-Wurzelordner: bash data/fetch.sh
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p raw
cd raw

# DS3: Penn World Table 11.0 (Feenstra, Inklaar, Timmer; GGDC), doi:10.34894/FABVLR, Datei pwt110.dta
curl -sSL -o pwt110.dta "https://dataverse.nl/api/access/datafile/554030"

# DS2: Maddison Project Database 2023 (Bolt, van Zanden), doi:10.34894/INZBF2, Datei maddison2023_web.dta
curl -sSL -o maddison2023_web.dta "https://dataverse.nl/api/access/datafile/421303"

# DS4: OECD, GERD nach Sektor und Art der Forschung; MSTI GERD in % des BIP
OECD="https://sdmx.oecd.org/public/rest/data"
H="Accept: application/vnd.sdmx.data+csv; charset=utf-8"
curl -sS -H "$H" -o oecd_gerd_tord.csv "$OECD/OECD.STI.STP,DSD_RDS_GERD@DF_GERD_TORD,/DEU+JPN+KOR+CHN+USA.........."
curl -sS -H "$H" -o oecd_msti_gerd_gdp.csv "$OECD/OECD.STI.STP,DSD_MSTI@DF_MSTI,/DEU+JPN+KOR+CHN+USA.A.G.PT_B1GQ.."

# DS5: Weltbank WDI, Lizenzgebuehren (Einnahmen, Zahlungen) und BIP in laufenden US-Dollar
for s in BX.GSR.ROYL.CD BM.GSR.ROYL.CD NY.GDP.MKTP.CD; do
  curl -sS -o "wb_$s.json" "https://api.worldbank.org/v2/country/DEU;JPN;KOR;CHN;USA;GBR/indicator/$s?format=json&per_page=2000"
done

# Drittmaerkte: CEPII TRADHIST v4 (Fouquin und Hugot 2016), ca. 1,1 GB
curl -sSL -o TRADHIST_v4.dta "https://www.cepii.fr/DATA_DOWNLOAD/TRADHIST/TRADHIST_v4.dta"

sha256sum TRADHIST_v4.dta pwt110.dta maddison2023_web.dta oecd_*.csv wb_*.json > SHA256SUMS.abruf

# Gutachten: US-Einfuhren je Warengruppe (Comtrade) und Konkordanzen HS -> SITC (WITS)
python3 data/population_fetch.py
python3 data/population_fetch_s3.py
python3 data/population_fetch_hs.py
python3 data/population_fetch_usimports.py
mkdir -p data/raw/wits && for c in S1 S3; do
  curl -s -o data/raw/wits/H0_$c.zip https://wits.worldbank.org/data/public/concordance/Concordance_H0_to_$c.zip
  (mkdir -p data/raw/wits/H0_$c && cd data/raw/wits/H0_$c && unzip -oq ../H0_$c.zip)
done
# Gutachten: Beschaeftigung (NBER-CES, NAICS 1997) und Census-Konkordanz der Einfuhrwaren 2002
mkdir -p data/raw/nberces data/raw/census
curl -s -o data/raw/nberces/n1997.csv https://data.nber.org/nberces/nberces5818v1/nberces5818v1_n1997.csv
curl -s -o data/raw/census/impconcord02.xls https://www.census.gov/foreign-trade/reference/codes/concordance/impconcord02.xls
# Kongressmessung (govinfo-API, Schluessel api.data.gov im Header X-Api-Key; setzt der Netzwerk-Proxy ein):
# taeglicher Congressional Record 1995-2025, gebundener Record 1955-1994 (Stichprobe), 301-Listen (Federal Register)
python3 data/crec_fetch.py all
python3 data/crecb_fetch.py 1955 1994
python3 data/fr301_lists.py
# Prueffsummen: je Datei in data/raw/crec(b)/MANIFEST.sha256, deren Summe und die FR-Dateien in SHA256SUMS.abruf
for d in crec crecb; do (cd data/raw/$d && find . -type f ! -name MANIFEST.sha256 | sort | xargs sha256sum > MANIFEST.sha256); done
(cd data/raw && sha256sum fr/*.pdf fr/*.htm crec/MANIFEST.sha256 crecb/MANIFEST.sha256 >> SHA256SUMS.abruf)
# Register AD/CVD/Safeguards: TTBD (Bown; Weltbank-Datenkatalog 0039583)
mkdir -p data/raw/ttbd && (cd data/raw/ttbd && for f in DR0049162/ttbd-gad.zip DR0049163/ttbd-gcvd.zip; do
  curl -sSL -O "https://datacatalogfiles.worldbank.org/ddh-published/0039583/1/$f"; done
  for z in gad gcvd; do mkdir -p $z && (cd $z && unzip -oq ../ttbd-$z.zip); done)
# Weitere Faelle (TH, VN, MY, MX, BR, HK, TW): Comtrade-Ausfuhren, Spiegeldaten Taiwan, US-Einfuhren, HK-Wiederausfuhren
python3 data/cases_fetch.py exports
python3 data/cases_fetch.py mirror
python3 data/cases_fetch.py usimports
python3 data/cases_fetch.py hkrx
# Japan gegen Grossbritannien 1920-1939: TRADHIST (oben), Hansard
python3 data/hansard_japan.py 1920 1939
# Politisch-militaerische Lage: COW NMC v7, ATOP 5.1, UNGA-Idealpunkte (Bailey, Strezhnev, Voeten; Juli 2025)
mkdir -p data/raw/geo/unga && (cd data/raw/geo && curl -sSL -O https://correlatesofwar.org/wp-content/uploads/NMCv7.zip \
  && unzip -oq NMCv7.zip -d nmc && (cd nmc/NMCv7 && unzip -oq NMC-v7-abridged.zip) \
  && curl -sSL -o atop51csv.zip "http://www.atopdata.org/uploads/6/9/1/3/69134503/atop_5.1__.csv_.zip" && unzip -oq atop51csv.zip -d atop \
  && curl -sSL -o unga/IdealpointsJuly2025.tab "https://dataverse.harvard.edu/api/access/datafile/11824371")
python3 data/geopolitics.py
# IWF-Auflagen, US-Hilfe, Sicherheitsrat (Harvard Dataverse; Stubbs et al. 2020 und 2016)
mkdir -p data/raw/imf && (cd data/raw/imf && curl -sSL -o IMFMETH_Data.dta "https://dataverse.harvard.edu/api/access/datafile/4576459?format=original" \
  && curl -sSL -o IMFAIDData.dta "https://dataverse.harvard.edu/api/access/datafile/4572529?format=original" \
  && curl -sSL -o IMFAIDCodebook.xlsx "https://dataverse.harvard.edu/api/access/datafile/4572527" \
  && curl -sSL -o IMFMETH_Code_Main.do "https://dataverse.harvard.edu/api/access/datafile/4576461")
python3 data/conditionality.py
