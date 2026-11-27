# Register sweep: coverage (27.11.2026)

Sweep of broad US trade measures (IR 4: quantity limits, OMAs, VRAs, sector-wide TRQs) against Japan (JP), Korea (KR) and China (CN), 1955-2024. Output: `register_sweep.csv` (20 rows: JP 8, KR 9, CN 3). `broad_register.csv` was not edited. Rows are only measures not already in B-01 to B-50, or only mentioned in a B-entry's note.

## Sources searched

| Source | Access | Years | What was done |
|---|---|---|---|
| Federal Register, govinfo (api.govinfo.gov search + issue PDFs, OCR via pdftotext) | yes | 1956-1993 | Sample sweep: up to 25 issues a year matching `"Japan" cotton textile` (1956-1973) or `"Japan" textile agreement` (1974-1993), and `"Korea" textile agreement` (1962-1993); about 1,400 issues read. Then targeted phrase searches: "textile products produced or manufactured in Japan" (1960-1994), "Textile Agreement" + "Government of Japan", "produced or manufactured in the Republic of Korea" around Dec 1977 and Dec 1982, "stainless steel table flatware" (1959-1972), China steel arrangement (1984-1992). Agreement dates were tabulated from every CITA or ITAC notice in the sample. |
| Federal Register, federalregister.gov API (agency = CITA) + govinfo HTML | yes | 1994-2026 | All CITA documents naming Korea (62), Japan (5) and China (all titles, 1994-2005) listed; the agreement-establishing notices read. |
| Presidential proclamations in the FR | yes | 1959; 2000-2003 | Proclamations 3323, 7273, 7274, 7585 read. |
| USITC, Import Injury Investigations Case Statistics (Feb 2010), Tables 14-17 | yes | FY 1975-2008 | All 201, 203, 421 and 406 cases with affirmative findings checked against relief. |
| USITC Pub. 850, History and Current Status of the MFA (Jan 1978) | yes | 1957-1977 | Japan and Korea agreement chronology (pp. 1, 48-50). |
| USITC Pubs. 1942, 1953, 1984, 2007 (steel monthly reports 1987), 1962 (specialty steel), 2182 (steel VRAs, 1989) | yes | 1987-1989 | Lists of countries with steel VRAs (China). |
| Repository files `nonallied_measures_pre1995.csv`, `new_china_safeguards.csv` | yes | - | China rows not duplicated. |

## What could not be searched

- OTEXA archives (otexa.trade.gov): blocked by the proxy (HTTP 403). No category-level quota histories.
- State Department (state.gov, Treaties in Force), HathiTrust, NARA catalogue: blocked. UST/TIAS texts of the bilateral textile agreements not seen; signature dates come from the FR or USITC Pub. 850.
- Japan's textile agreements 1963-1979 were run through Japanese export licensing and seldom appear in the FR. The 1972 and 1974 Japan rows rest on USITC Pub. 850 only.
- The FR sample for 1962-1993 is a sample (25 issues a year), not a full read. Agreement changes are well covered because every notice cites the agreement in force. Single calls within an agreement are not complete, and they were not entered as separate measures (see below).
- OCR of the historical FR mixes columns. Page numbers are given where the OCR showed them; otherwise volume and issue date.
- Section 201 cases after FY 2008 were not checked against a case list (B-18 covers 2018). Pre-1975 escape-clause cases (1951-1974) were not searched one by one; only stainless steel flatware (1959) was checked.
- The text of the China steel VRA and its signature month were not found.

## Decisions on scope (not added as rows)

- **Calls and consultations within an agreement** (e.g. Korea 1983 Cats 300/301, Japan 1984 Cats 314/604/644, China calls 1984-1987) are part of the agreement row. The exceptions are calls that ended in unilateral limits after a breakdown: Japan 1986 is a row.
- **Tariff-only relief (IR 3)**, verified as affirmative in USITC Table 14 but not entered: CB radios 1978 (JP, KR, TW); bolts, nuts and screws 1979 (JP); porcelain-on-steel cookware 1980; mushrooms 1980; tyres 421 2009 (CN, already in `new_china_safeguards.csv`). Supplier lists for these were not checked.
- **China para. 242 textile safeguards 2003-2005** (CN-S01 to CN-S05): scored IR 3 in `new_china_safeguards.csv`; not repeated.
- **Global quotas not naming JP, KR or CN**: steel wire rod TRQ 2000 (Proclamation 7273: "all countries" except Canada and Mexico), clothespins 1979, wheat gluten 1998, lamb 1999. Not entered. Flatware 1959 and line pipe 2000 are in the CSV marked `candidate (scope)` because they bear on the first year of a rung or lead to a measure naming Korea.
- **Renewals of non-textile measures** already in the register (steel VRA 1969 renewal 1972, car VER extensions 1984-1994, steel VRA extension 1989-1992, semiconductor agreement 1991): treated as part of B-03, B-10, B-13 and B-14.
- **Korea 1963 restraints and the 1965 cotton agreement, Japan 1963 agreement**: already in the B-02 note; not repeated.

## Existing entries confirmed in this sweep

B-01 and B-02 (Pub. 850: Japanese controls from 1957; Japan LTA agreement effective 1 Jan 1963; Korea restraints from 1963 and 3-year agreement from 1 Jan 1965), B-04 (FR: Korea wool/MMF agreement of 4 Jan 1972, five years from 1 Oct 1971; Pub. 850: Japan from 1 Oct 1971), B-05, B-06, B-07/B-08, B-11, B-12, B-13, B-17 (USITC Table 14 cases 5, 18, 19, 47, 48, 51, 73 affirmative), B-13 (Pub. 2182 lists Japan and Korea among VRA countries), B-47 (Table 17 case 11), B-49 (successor MOU of 1997 confirms the 1994-1996 term).
