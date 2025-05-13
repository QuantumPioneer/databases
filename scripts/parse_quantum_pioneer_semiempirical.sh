#!/bin/bash

DIR=/home/gridsan/groups/qmdata/quantumpioneer

conda create -n quantumpioneer -y
conda activate quantumpioneer

cd $DIR/FastLogfileParser
pip install -e .

cd $DIR/databases
pip install -e .

cd $DIR/databases/scripts
sbatch generate_db.slurm semiempirical "_ts" $DIR/ts_semiempirical_log_files.txt
sbatch generate_db.slurm semiempirical "_nonts" $DIR/nonts_semiempirical_log_files.txt
