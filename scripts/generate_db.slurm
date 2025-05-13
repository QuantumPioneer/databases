#!/bin/bash -l
#SBATCH -J generate_dbs
#SBATCH -t 02-00:00:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH -N 1
#SBATCH --exclusive
#SBATCH --mem=192000


# USER INPUT: before running, run log_finder.sh to generate a list of logfile.
# can be either dft, dlpno, or cosmo
# run this script with 'sbatch generate_db.slurm {dlpno,dft,cosmo} {db_name_suffix} {logfile_fpath}'
# where the latter two are optional
DB_TYPE=$1
DB_NAME_SUFFIX=$2
LOGFILES_LIST=$3

module purge
module load anaconda
source activate quantumpioneer

# make outdir if needed
NODE_PATH=/state/partition1/user/$USER/
mkdir -p $NODE_PATH
DB_NAME=$DB_TYPE$DB_NAME_SUFFIX.parquet
DB_PATH=$NODE_PATH$DB_NAME

cd /home/gridsan/$USER/QuantumPioneer/databases/databases
python generator.py $LOGFILES_LIST $DB_PATH $DB_TYPE

# after all that, run this command to compress the hell out of the database file:
XZ_OPT='-v -e9 --threads=0' tar cJfv $NODE_PATH$DB_NAME.tar.xz -C $NODE_PATH $DB_NAME

# then move it to the shared directory
DEST=/home/gridsan/groups/qmdata/quantumpioneer/databases/scripts/
rsync -va --progress $NODE_PATH$DB_NAME.tar.xz $DEST$DB_NAME.tar.xz

# and decompress it
cd $DEST
tar -xvf $DB_NAME.tar.xz

# clean up the node
rm -rf $NODE_PATH
