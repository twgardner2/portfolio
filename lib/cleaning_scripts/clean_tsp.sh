# Usage: run this script with the input file as the first argument,
# piping the output to a file where you want to save it:

# Ex: bash lib/cleaning_scripts/clean_tsp.sh awk/InvestmentActivityDetail_civ.csv > tsp_civ.csv

awk -f awk/tsp_to_trans.awk $1 | sort -k 2