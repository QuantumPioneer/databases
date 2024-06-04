# sys.argv:
# 1: text file listing all of the logfiles to read
# 2: database file to write to
# 3: type of database {dft,dlpno,cosmo}
import sys
from multiprocessing import Pool
from types import MappingProxyType

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


def _dft(fpath):
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


if __name__ == "__main__":
    all_logfile_fpaths = None
    with open(LOGFILE_PATHS_FILE, "r") as file:
        all_logfile_fpaths = file.read().splitlines()

    writer = pq.ParquetWriter(DB_PATH, SCHEMA_LOOKUP[DB_TYPE])
    with Pool(96) as p:
        with tqdm(
            total=len(all_logfile_fpaths),
            desc=f"Parsing {DB_TYPE}",
        ) as pbar:
            buffer = []
            for result in p.imap_unordered(_func_lookup[DB_TYPE], all_logfile_fpaths, 512):
                buffer.extend(result)
                if len(buffer) >= 512:
                    buffer = _dump_buffer(writer, buffer)
                pbar.update()

            # Write the remaining data
            if buffer:
                _dump_buffer(writer, buffer)
    writer.close()
