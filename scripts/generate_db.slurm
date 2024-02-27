#!/bin/bash -l
#SBATCH -J generate_dbs
#SBATCH -t 01-00:00:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH -N 1
#SBATCH --exclusive

# USER INPUT: before running, run log_finder.sh to generate a list of logfile.
# can be either dft, dlpno, or cosmo
# run this script with 'sbatch generate_db.slurm {dlpno,dft,cosmo}'
DB_TYPE=$1

# derived from above
LOGFILES_LIST=/home/gridsan/jburns/quantumpioneer/databases/scripts/all_${DB_TYPE}_log_files.txt

module purge
module load anaconda
source activate parser

# make outdir if needed
mkdir -p /state/partition1/user/jburns
DB_NAME=$DB_TYPE.db
NODE_PATH=/state/partition1/user/jburns/
DB_PATH=$NODE_PATH$DB_NAME

cd /home/gridsan/jburns/quantumpioneer/databases/databases
python generator.py $LOGFILES_LIST $DB_PATH

# after all that, run this command to compress the hell out of the database file:
XZ_OPT=-v XZ_OPT=-e9 XZ_OPT=--threads=0 tar cJfv $DB_NAME.tar.xz -C $NODE_PATH $DB_NAME

# then copy it off the node
DEST=/data1/groups/qmdata/
cp $DB_NAME.tar.xz $DB_NAME.tar.xz

# and decompress it
tar -xvf $DB_NAME.tar.xz -C DEST