# log_finder.sh
#
# Usage: bash log_finder.sh dir_1 dir_2 ... dir_n
# 
# Short bash script to find all the .log files stored in the given directories,
# results are written to stdout.

<<examples
Here are the commands used for the QuantumPioneer databases.

DFT data:
bash log_finder.sh \
    "/home/gridsan/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/DFT_opt_freq/outputs/" \
    "/home/gridsan/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/DFT_opt_freq/outputs/" \
    "/home/gridsan/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/DFT_opt_freq/outputs/" \
    "/home/gridsan/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/output/DFT_opt_freq/outputs/" \
    "/home/gridsan/groups/RMG/Projects/Habs/data/ts/dft/"  >> all_dft_log_files.txt

DLPNO data:
bash log_finder.sh \
    "/home/gridsan/jburns/co2_capture_shared/reactant_product_calculation/ts_nho_round1/output/DLPNO_sp_f12/outputs" \
    "/home/gridsan/jburns/RMG_shared/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/DLPNO_sp_f12/outputs" \
    "/home/gridsan/jburns/RMG_shared/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/DLPNO_sp_f12/outputs" \
    "/home/gridsan/jburns/RMG_shared/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/ts_calculations/calculations/sep1a/output/DLPNO_sp_f12/outputs" \
    "/home/gridsan/jburns/co2_capture_shared/ts_guess_generation/ts_dlpno_calculation_20231117/output/DLPNO_sp_f12/outputs" >> all_dlpno_log_files.txt

COSMO data:
bash log_finder.sh \
    "/home/gridsan/jburns/co2_capture_shared/cosmo_backup/cosmo_rp_aug11b_backup" \
    "/home/gridsan/jburns/co2_capture_shared/cosmo_backup/cosmo_rp_sep1a_backup" \
    "/home/gridsan/jburns/co2_capture_shared/reactant_product_calculation/ts_nho_round1/output/COSMO_calc" >> all_cosmo_log_files.txt

examples

for dir in "$@"; do
    find $dir -type f -name "*.log" | xargs realpath --no-symlinks
done