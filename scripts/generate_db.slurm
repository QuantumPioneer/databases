#!/bin/bash -l
#SBATCH -J generate_dbs
#SBATCH -t 01-00:00:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH -N 1
#SBATCH --exclusive

# before, also need to get a file that lists all of the logfiles to look at.
DB_TYPE=DLPNO
LOGFILES_LIST=/home/gridsan/jburns/quantumpioneer/databases/scripts/all_dlpno_log_files.txt

module purge
module load anaconda
source activate parser

# make outdir if needed
mkdir -p /state/partition1/user/jburns
DB_NAME=$DB_TYPE.db
NODE_PATH=/state/partition1/user/jburns/
DB_PATH=$NODE_PATH$DB_NAME

cd /home/gridsan/jburns/quantumpioneer/databases/databases
python generator.py $LOGFILES_LIST $DB_PATH $DB_TYPE

# after all that, run this command to compress the hell out of the database file:
XZ_OPT=-v XZ_OPT=-e9 XZ_OPT=--threads=0 tar cJfv $DB_NAME.tar.xz -C $NODE_PATH $DB_NAME

# then copy it off the node
cp $DB_NAME.tar.xz /home/gridsan/jburns/$DB_NAME.tar.xz
