#!/bin/bash -x
# Submit the logfile list generator
job1=$(sbatch generate_logfile_lists.slurm)

# Extract the job ID from the submission output
job1_id=$(echo $job1 | awk '{print $4}')

# Submit subsequent jobs dependent on that job

# everything to be submitted
# Gaussian logfiles
# ts_semi_logfiles.txt
# ts_dft_logfiles.txt
# nonts_semi_logfiles.txt
# nonts_dft_logfiles.txt
# nbo_logfiles.txt
# ORCA (DLPNO) Logfiles
# ts_dlpno_logfiles.txt
# nonts_dlpno_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dft "_ts_semi_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/ts_semi_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dft "_ts_dft_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/ts_dft_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dft "_nonts_semi_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/nonts_semi_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dft "_nonts_dft_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/nonts_dft_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dft "_nbo_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/nbo_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dlpno "_ts_dlpno_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/ts_dlpno_logfiles.txt
sbatch --dependency=afterok:$job1_id generate_db.slurm dlpno "_nonts_dlpno_v4" /home/gridsan/jburns/quantumpioneer/databases/scripts/nonts_dlpno_logfiles.txt
