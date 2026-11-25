#!/usr/bin/env bash
# Runs all analyses after `bash data/fetch.sh`. Call from the package root: bash data/run_all.sh
# The Hansard scripts download the Historic Hansard pages on first run and take several hours.
set -euo pipefail
cd "$(dirname "$0")/.."
run() { echo ">> $1"; python3 "data/$1" "${@:2}"; }
# Core datasets (DS1 events from milestones and responses; DS2-DS5 from raw files)
run build.py
# British parliamentary attention (Appendix E, F; Table 4 panel A)
run hansard_salience.py; run hansard_competition.py; run hansard_sectors.py; run hansard_usa.py; run hansard_phrases.py
run hansard_japan.py 1920 1939
# Trade: third markets, export milestones, registers (Appendices B, D, G)
run third_markets.py; run third_markets_1930s.py; run comtrade_milestones.py
run registers_ttbd.py; run registers_product_displacement.py
# Population of manufacturing groups, panel, weights (Table 3, Appendix D)
run population_test.py; run population_panel.py; run population_employment.py
# Congressional Record (Table 4 panel B, Appendix I)
run crec_salience.py; run crec_sectors.py; run crec_controls.py
run crecb_salience.py; run crecb_korea.py; run crecb_share.py; run crecb_controls.py
# Further cases, alignment, conditionality (Appendices G, H)
run cases_test.py; run geopolitics.py; run conditionality.py
run robust_broad.py
# Sequence and business-cycle tests (Section 4, Appendix C)
run tests_sequence.py; run tests_cycle.py
# Figures
python3 manuscript/figures/fig_story.py; python3 manuscript/figures/fig_e1.py; python3 manuscript/figures/fig_e2_crec.py
