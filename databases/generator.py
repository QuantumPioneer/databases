# sys.argv:
# 1: text file listing all of the logfiles to read
# 2: database file to write to
# 3: type of database {dft,dlpno,cosmo}
import sys
import pickle
from multiprocessing import Pool
from pathlib import Path

# dill, peewee, tqdm, and fglp are all single-library dependencies
from tqdm import tqdm
from fastlogfileparser.gaussian import fast_gaussian_logfile_parser as fglp
from fastlogfileparser.orca import fast_orca_logfile_parser as folp
import numpy as np

from schema import PLACEHOLDER_DB, DLPNOResults, DFTResults

LOGFILE_PATHS_FILE = sys.argv[1]
DB_PATH = sys.argv[2]
DB_TYPE = sys.argv[3]


def _blobify(arr):
    try:
        return pickle.dumps(arr)
    except Exception as e:
        return "Err: " + str(e)


FIELDS = None
INSERT_FUNC = None
RESULTS_TABLE = None
if DB_TYPE == "dlpno":

    def INSERT_FUNC(fpath):
        (result,) = folp(fpath)
        return ((
            fpath,
            result.route_section,
            result.charge_and_multiplicity[0],
            result.charge_and_multiplicity[1],
            result.energy,
            result.run_time,
            _blobify(result.input_coordinates),
        ), )

    FIELDS = [
        DLPNOResults.source,
        DLPNOResults.route_section,
        DLPNOResults.charge,
        DLPNOResults.multiplicity,
        DLPNOResults.energy,
        DLPNOResults.run_time,
        DLPNOResults.input_coordinates,
    ]
    RESULTS_TABLE = DLPNOResults

elif DB_TYPE == "dft":

    def INSERT_FUNC(fpath):
        job_tuple = fglp(fpath, include_intermediates=False)
        return ((
            fpath,
            result.route_section,
            result.charge_and_multiplicity[0],
            result.charge_and_multiplicity[1],
            result.max_steps,
            result.normal_termination,
            result.cpu_time,
            result.wall_time,
            result.e0_h,
            result.hf,
            result.zpe_per_atom,
            result.e0_zpe,
            result.gibbs,
            _blobify(result.scf),
            _blobify(result.recovered_energy),
            _blobify(result.frequency_modes),
            _blobify(result.frequencies),
            _blobify(result.std_forces),
            _blobify(result.std_xyz),
            _blobify(result.xyz),
        ) for result in job_tuple)

    FIELDS = [
        DFTResults.source,
        DFTResults.route_section,
        DFTResults.charge,
        DFTResults.multiplicity,
        DFTResults.max_steps,
        DFTResults.normal_termination,
        DFTResults.cpu_time,
        DFTResults.wall_time,
        DFTResults.e0_h,
        DFTResults.hf,
        DFTResults.zpe_per_atom,
        DFTResults.e0_zpe,
        DFTResults.gibbs,
        DFTResults.scf,
        DFTResults.recovered_energy,
        DFTResults.frequency_modes,
        DFTResults.frequencies,
        DFTResults.std_forces,
        DFTResults.std_xyz,
        DFTResults.xyz,
    ]
    RESULTS_TABLE = DFTResults


def _parallel_parser_helper(fpath_batch):
    to_insert = []
    for fpath in fpath_batch:
        try:
            to_insert.extend(INSERT_FUNC(fpath))
        except Exception as e:
            print("Parse Error", fpath, str(e), sep="::")
    return to_insert


PLACEHOLDER_DB.init(DB_PATH)
PLACEHOLDER_DB.connect()
PLACEHOLDER_DB.create_tables([RESULTS_TABLE])

all_logfile_fpaths = None
with open(LOGFILE_PATHS_FILE, "r") as file:
    all_logfile_paths = file.read().splitlines()
n_per_batch = 128
n_batches = len(all_logfile_paths) // n_per_batch
batched_logfile_paths = np.array_split(all_logfile_paths, n_batches)
del all_logfile_paths

with Pool(96) as p:
    with tqdm(total=n_batches) as pbar:
        for result in p.imap_unordered(
            _parallel_parser_helper, batched_logfile_paths, 1
        ):
            RESULTS_TABLE.insert_many(result, fields=FIELDS).execute()
            pbar.update()
PLACEHOLDER_DB.close()
