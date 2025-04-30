# sys.argv:
# 1: text file listing all of the logfiles to read
# 2: database file to write to
# 3: type of database {dft,dlpno,cosmo}
import sys
from multiprocessing import Pool
from types import MappingProxyType
from contextlib import closing

import pyarrow as pa
import pyarrow.parquet as pq
from fastlogfileparser.gaussian import fast_gaussian_logfile_parser as fglp
from fastlogfileparser.orca import fast_orca_logfile_parser as folp
from schema import SCHEMA_LOOKUP

from tqdm import tqdm

LOGFILE_PATHS_FILE = sys.argv[1]
DB_PATH = sys.argv[2]
DB_TYPE = sys.argv[3]


def _dlpno(fpath):
    try:
        (result,) = folp(fpath)
        return [
            {
                "energy": result.energy,
                "run_time": result.run_time,
                "input_coordinates": result.input_coordinates,
                "source": fpath,
                "route_section": result.route_section,
                "charge": result.charge_and_multiplicity[0],
                "multiplicity": result.charge_and_multiplicity[1],
            }
        ]
    except Exception as e:
        print(f"Unable to parse {fpath}, exception: {str(e)}")
        return []


def _dft(fpath):
    try:
        return [
            {
                "source": fpath,
                "route_section": result.route_section,
                "charge": result.charge_and_multiplicity[0],
                "multiplicity": result.charge_and_multiplicity[1],
                "max_steps": result.max_steps,
                "normal_termination": result.normal_termination,
                "cpu_time": result.cpu_time,
                "wall_time": result.wall_time,
                "e0_h": result.e0_h,
                "hf": result.hf,
                "zpe_per_atom": result.zpe_per_atom,
                "e0_zpe": result.e0_zpe,
                "gibbs": result.gibbs,
                "scf": result.scf,
                "frequencies": result.frequencies,
                "frequency_modes": result.frequency_modes,
                "xyz": result.xyz,
                "std_xyz": result.std_xyz,
                "std_forces": result.std_forces,
            }
            for result in fglp(fpath)
        ]
    except Exception as e:
        print(f"Unable to parse {fpath}, exception: {str(e)}")
        return []


_func_lookup: MappingProxyType = MappingProxyType(
    {
        "dlpno": _dlpno,
        "dft": _dft,
    }
)


def _dump_buffer(writer: pq.ParquetWriter, buffer: list[dict]):
    table = pa.Table.from_pylist(buffer, schema=SCHEMA_LOOKUP[DB_TYPE])
    writer.write_table(table)
    return []


BUFFER_SIZE = 32
CHUNK_SIZE = 20000


def chunks(lst, n):
    """Yield n chunks"""
    for i in range(n):
        yield lst[i * CHUNK_SIZE : (i + 1) * CHUNK_SIZE]


if __name__ == "__main__":
    all_logfile_fpaths = None
    with open(LOGFILE_PATHS_FILE, "r") as file:
        all_logfile_fpaths = file.read().splitlines()

    num_chunks = (len(all_logfile_fpaths) + CHUNK_SIZE - 1) // CHUNK_SIZE
    writer = pq.ParquetWriter(DB_PATH, SCHEMA_LOOKUP[DB_TYPE])
    for k, logfile_fpaths in enumerate(chunks(all_logfile_fpaths, num_chunks)):
        with closing(Pool(96)) as p:
            with tqdm(
                total=len(logfile_fpaths),
                desc=f"Parsing {DB_TYPE} (chunk {k+1}/{num_chunks})",
            ) as pbar:
                buffer = []
                for result in p.imap_unordered(_func_lookup[DB_TYPE], logfile_fpaths, BUFFER_SIZE):
                    buffer.extend(result)
                    if len(buffer) >= BUFFER_SIZE:
                        buffer = _dump_buffer(writer, buffer)
                    pbar.update()

                # Write the remaining data
                if buffer:
                    _dump_buffer(writer, buffer)
    writer.close()
