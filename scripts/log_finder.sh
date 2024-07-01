# log_finder.sh
#
# Usage: bash log_finder.sh dir_1 dir_2 ... dir_n
# 
# Short bash script to find all the .log files stored in the given directories,
# results are written to stdout.
#
# All of the filepaths provided to this script should use 'realpath' first to
# make sharing file locations easier.

<<examples
Here are the commands used for the QuantumPioneer databases.

DFT data:
bash log_finder.sh \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/DFT_opt_freq/outputs/" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/semiempirical_opt/outputs/" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/DFT_opt_freq/outputs/" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/semiempirical_opt/outputs/" \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/semiempirical_opt/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/generated_ts_guesses/" \
    "/data1/groups/RMG/Projects/Habs/data/ts/semi/" \
    "/data1/groups/RMG/Projects/Habs/data/ts/dft/"  >> all_dft_log_files.txt

DLPNO data:
bash log_finder.sh \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/DLPNO_sp_f12/outputs" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/DLPNO_sp_f12/outputs" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/DLPNO_sp_f12/outputs" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/ts_calculations/calculations/sep1a/output/DLPNO_sp_f12/outputs" \
    "/data1/groups/co2_capture/ts_guess_generation/ts_dlpno_calculation_20231117/output/DLPNO_sp_f12/outputs" >> all_dlpno_log_files.txt

COSMO data:
bash log_finder.sh \
    "/data1/groups/co2_capture/cosmo_backup/cosmo_rp_aug11b_backup" \
    "/data1/groups/co2_capture/cosmo_backup/cosmo_rp_sep1a_backup" \
    "/data1/groups/co2_capture/cosmo_backup/cosmo_ts_sep1a_backup" \
    "/data1/groups/co2_capture/ts_guess_generation/ts_dlpno_calculation_20231117/output/COSMO_calc" \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/COSMO_calc" >> all_cosmo_log_files.txt

examples

for dir in "$@"; do
    find $dir -type f -name "*.log"
done