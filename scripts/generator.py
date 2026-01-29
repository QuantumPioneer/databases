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
                "dipole_au": result.dipole_au,
                "t1_diagnostic": result.t1_diagnostic,
            }
        ]
    except Exception as e:
        print(f"Unable to parse {fpath}, exception: {str(e)}")
        return []


def _dft(fpath):
    try:
        results = fglp(fpath)
    except Exception as e:
        print(f"Unable to parse {fpath}, exception: {str(e)}. Skipping!")
        return []

    # this is how the results are actually split up
    # if len(results) == 3:  # semi-empirical
    #     am1_result, pm7_result, xtb_result = results
    # elif len(results) == 1:  # DFT
    #     dft_result = results[0]
    # else:
    #     print(f"Unexpected number of results in file {fpath}, skipping.")
    #     return []
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
                "dipole_au": result.dipole_au,
                "aniso_polarizability_au": result.aniso_polarizability_au,
                "iso_polarizability_au": result.iso_polarizability_au,
                "dipole_moment_debye": result.dipole_moment_debye,
                "mulliken_charges_summed": (
                    None  # avoid attempting to index None if this is missing
                    if result.mulliken_charges_summed is None
                    # if printed twice, take the second one
                    else (
                        result.mulliken_charges_summed[-1]
                        if isinstance(result.mulliken_charges_summed[0][0], list)
                        else result.mulliken_charges_summed
                    )
                ),
                # "mulliken_charges_spin_densities_summed": (
                #     None  # avoid attempting to index None if this is missing
                #     if result.mulliken_charges_spin_densities_summed is None
                #     # if printed twice, take the second one
                #     else (
                #         result.mulliken_charges_spin_densities_summed[-1]
                #         if isinstance(result.mulliken_charges_spin_densities_summed[0][0], list)
                #         else result.mulliken_charges_spin_densities_summed
                #     )
                # ),
                "homo_lumo_gap": result.homo_lumo_gap,
                "beta_homo_lumo_gap": result.beta_homo_lumo_gap,
                "scf": result.scf,
                "frequencies": result.frequencies,
                "nmr_shielding": result.nmr_shielding,
                "frequency_modes": result.frequency_modes,
                "xyz": result.xyz[-1],  # keep only the converged XYZ
                "std_xyz": result.std_xyz[-5:],  # keep only the last 5 steps of optimization
                "std_forces": None if result.std_forces is None else result.std_forces[-5:],
            }
            for result in results
            if results[-1].normal_termination  # skip entire composite job if DFT failed
        ]
    except Exception as e:
        print(f"Unable to munge {fpath}, exception: {str(e.with_traceback(e.__traceback__))}. Skipping!")
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
