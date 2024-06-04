#!/bin/bash -l
#SBATCH -J generate_dbs
#SBATCH -t 02-00:00:00
#SBATCH -o slurm.%j.out
#SBATCH -e slurm.%j.err
#SBATCH -N 1
#SBATCH --exclusive


# USER INPUT: before running, run log_finder.sh to generate a list of logfile.
# can be either dft, dlpno, or cosmo
# run this script with 'sbatch generate_db.slurm {dlpno,dft,cosmo} {db_name_suffix} {logfile_fpath}'
# where the latter two are optional
DB_TYPE=$1
DB_NAME_SUFFIX=$2
LOGFILES_LIST=$3

# derived from above if not explicitly passed
if [ -z "${LOGFILES_LIST}" ]; then
    LOGFILES_LIST=/home/gridsan/jburns/quantumpioneer/databases/scripts/all_${DB_TYPE}_log_files.txt
fi

module purge
module load anaconda
source activate parser

# make outdir if needed
NODE_PATH=/state/partition1/user/jburns/
mkdir -p $NODE_PATH
DB_NAME=$DB_TYPE$DB_NAME_SUFFIX.db
DB_PATH=$NODE_PATH$DB_NAME

cd /home/gridsan/jburns/quantumpioneer/databases/databases
python generator.py $LOGFILES_LIST $DB_TYPE $DB_PATH

# after all that, run this command to compress the hell out of the database file:
XZ_OPT=-v XZ_OPT=-e9 XZ_OPT=--threads=0 tar cJfv $DB_NAME.tar.xz -C $NODE_PATH $DB_NAME

# then move it to the shared directory
DEST=/data1/groups/qmdata/
mv $DB_NAME.tar.xz $DEST$DB_NAME.tar.xz

# and decompress it
cd $DEST
tar -xvf $DB_NAME.tar.xz

# clean up the node
rm -rf $NODE_PATH
