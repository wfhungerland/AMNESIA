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
python3 data/population_fetch_usimports.py
mkdir -p data/raw/wits && for c in S1 S3; do
  curl -s -o data/raw/wits/H0_$c.zip https://wits.worldbank.org/data/public/concordance/Concordance_H0_to_$c.zip
  (mkdir -p data/raw/wits/H0_$c && cd data/raw/wits/H0_$c && unzip -oq ../H0_$c.zip)
done
