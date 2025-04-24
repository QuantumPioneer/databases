# Defines the schema for the QuantumPioneer databases
from copy import deepcopy
from types import MappingProxyType

import pyarrow as pa

_base_results = pa.schema(
    [
        ("source", pa.utf8()),
        ("route_section", pa.utf8()),
        ("charge", pa.uint8()),
        ("multiplicity", pa.uint8()),
    ],
    metadata={
        "source": "Original file",
        "route_section": "Level of theory",
        "charge": "Molecular formal charge",
        "multiplicity": "Electron multiplicity",
    },
)

DLPNO_SCHEMA: pa.Schema = pa.unify_schemas(
    [
        _base_results,
        pa.schema(
            [
                ("energy", pa.float64()),
                ("run_time", pa.uint32()),
                ("input_coordinates", pa.list_(pa.list_(pa.float64()))),
            ],
            metadata={
                "energy": "Total energy",
                "run_time": "Execution time in seconds",
                "input_coordinates": "XYZ coordinates at input",
            },
        ),
    ]
)

DFT_SCHEMA: pa.Schema = pa.unify_schemas(
    [
        _base_results,
        pa.schema(
            [
                ("max_steps", pa.uint32()),
                ("normal_termination", pa.bool_()),
                ("cpu_time", pa.uint32()),
                ("wall_time", pa.uint32()),
                ("e0_h", pa.float64()),
                ("hf", pa.float64()),
                ("zpe_per_atom", pa.float64()),
                ("e0_zpe", pa.float64()),
                ("gibbs", pa.float64()),
                ("scf", pa.list_(pa.float64())),
                ("frequencies", pa.list_(pa.float64())),
                ("frequency_modes", pa.list_(pa.list_(pa.list_(pa.float64())))),
                ("xyz", pa.list_(pa.list_(pa.list_(pa.float64())))),
                ("std_xyz", pa.list_(pa.list_(pa.list_(pa.float64())))),
                ("std_forces", pa.list_(pa.list_(pa.list_(pa.float64())))),
            ],
            metadata={
                "max_steps": "Maximum allowed steps",
                "normal_termination": "Terminated normally",
                "cpu_time": "CPU time in seconds",
                "wall_time": "Wall time in seconds",
                "e0_h": "Enthalpy at 298K",
                "hf": "E0 for non-wavefunction methods",
                "zpe_per_atom": "Per-atom zero point energy",
                "e0_zpe": "Gibbs free energy at 0K",
                "gibbs": "Gibbs free energy at 298K",
                "scf": "SCF energy",
                "frequencies": "Vibrational frequencies",
                "frequency_modes": "Vibrational modes",
                "xyz": "Input XYZ coords",
                "std_xyz": "Standardized XYZ coords",
                "std_forces": "Standardized forces",
            },
        ),
    ]
)

SCHEMA_LOOKUP: MappingProxyType = MappingProxyType(
    {
        "dlpno": DLPNO_SCHEMA,
        "cosmo": DLPNO_SCHEMA,
        "dft": DFT_SCHEMA,
        "semiempirical": DFT_SCHEMA,
    }
)
