#!/bin/bash -l
#SBATCH -J logfiles
#SBATCH -t 02-00:00:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH -N 1
#SBATCH --exclusive

cd /home/gridsan/jburns/quantumpioneer/databases/scripts

bash log_finder.sh \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/DFT_opt_freq/outputs/" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/generated_ts_guesses/" \
    "/data1/groups/RMG/Projects/Habs/data/ts/dft/"  >> all_reactants_products_log_files.txt

bash log_finder.sh \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/output/DFT_opt_freq/outputs/" \
    "/data1/groups/co2_capture/ts_guess_generation/nho_oho_ts_guess_generation_20220524/generated_ts_guesses/" \
    "/data1/groups/RMG/Projects/Habs/data/ts/dft/"  >> all_ts_log_files.txt

bash log_finder.sh \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/aug11b/output/semiempirical_opt/outputs/" \
    "/data1/groups/RMG/Projects/Hao-Wei-Oscar-Yunsie/HAbs_calculations/reactants_products_calculations/calculations/sep1a_filtered/output/semiempirical_opt/outputs/" \
    "/data1/groups/co2_capture/reactant_product_calculation/ts_nho_round1/output/semiempirical_opt/outputs/" >> nonts_semi_log_files.txt

bash log_finder.sh \
    "/data1/groups/RMG/Projects/Habs/data/ts/semi/"  >> ts_semi_log_files.txt
