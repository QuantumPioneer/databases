# sys.argv:
# 1: text file listing all of the logfiles to read
# 2: database file to write to
# 3: type of data in the logfiles
#
import os
import sys
import pickle
from multiprocessing import Pool

# dill, peewee, tqdm, and fglp are all single-library dependencies
import dill
from peewee import SqliteDatabase, Model, BlobField, TextField, FloatField, IntegerField, BooleanField
from tqdm import tqdm
from fastlogfileparser.orca import fast_orca_logfile_parser as folp
from fastlogfileparser.orca.fast_orca_logfile_parser import ALL_FIELDS
import numpy as np

from schema import PLACEHOLDER_DB, DLPNOResults

def _blobify(arr):
    try:
        return pickle.dumps(arr)
    except Exception as e:
        return "Err: " + str(e)

def _parallel_parser_helper(fpath_batch):
    to_insert = []
    for fpath in fpath_batch:
        try:
            # TODO: change this based on the log file type
            (result,) = folp(fpath)
            to_insert.append(
                (
                    fpath,
                    result.route_section,
                    result.charge_and_multiplicity[0],
                    result.charge_and_multiplicity[1],
                    result.energy,
                    result.run_time,
                    _blobify(result.input_coordinates),
                )
            )

        except Exception as e:
            print("Parse Error", fpath, str(e), sep="::")
    return to_insert

# db = SqliteDatabase()
PLACEHOLDER_DB.init(sys.argv[2])
PLACEHOLDER_DB.connect()
PLACEHOLDER_DB.create_tables([DLPNOResults])

all_logfile_fpaths = None
with open(sys.argv[1], "r") as file:
    all_logfile_paths = file.read().splitlines()
n_per_batch = 128
n_batches = len(all_logfile_paths) // n_per_batch
batched_logfile_paths = np.array_split(all_logfile_paths, n_batches)
del all_logfile_paths

with Pool(47) as p:
    with tqdm(total=n_batches) as pbar:
        for result in p.imap_unordered(_parallel_parser_helper, batched_logfile_paths, 1):
            DLPNOResults.insert_many(
                result,
                fields=[
                    DLPNOResults.source,
                    DLPNOResults.route_section,
                    DLPNOResults.charge,
                    DLPNOResults.multiplicity,
                    DLPNOResults.energy,
                    DLPNOResults.run_time,
                    DLPNOResults.input_coordinates,
                ],
            ).execute()
            pbar.update()
PLACEHOLDER_DB.close()