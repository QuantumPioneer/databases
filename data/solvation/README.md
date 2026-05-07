# QuantumPioneer Solvation Dataset

Computed solvation free energies and enthalpies at 298.15 K for solute–solvent pairs, generated
by the COSMO-RS-based workflow described in the QuantumPioneer project paper. Each CSV file
corresponds to a single solvent (295 solvents total) and contains solvation properties for
every solute evaluated in that solvent.

## Closed-Shell Species, Open-Shell Species, and Transition States

| Column   | Type   | Units    | Description                                                     |
|:---------|:------:|:--------:|:----------------------------------------------------------------|
| `smiles` | string | —        | Canonical SMILES of the solute                                  |
| `Gsolv`  | number | kcal/mol | Solvation free energy of the solute in this solvent at 298.15 K |
| `Hsolv`  | number | kcal/mol | Solvation enthalpy of the solute in this solvent at 298.15 K    |

**Note:** The transition states are represented as reaction SMILES (`r1.r2>>p1.p2`).

## Reactions

| Column            | Type   | Units    | Description                                                                |
|:------------------|:------:|:--------:|:---------------------------------------------------------------------------|
| `rxn_smiles`      | string | —        | Reaction SMILES (`r1.r2>>p1.p2`)                                           |
| `DDGsolv_forward` | number | kcal/mol | Solvation free energy of activation in the forward direction (`r1.r2>>ts`) |
| `DDGsolv_reverse` | number | kcal/mol | Solvation free energy of activation in the reverse direction (`p1.p2>>ts`) |
| `DDHsolv_forward` | number | kcal/mol | Solvation enthalpy of activation in the forward direction (`r1.r2>>ts`)    |
| `DDHsolv_reverse` | number | kcal/mol | Solvation enthalpy of activation in the reverse direction (`p1.p2>>ts`)    |

All energies are in kcal/mol.

## Directory Structure

```
├── quantumpioneer_solvation_dataset_closed_shell_species/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   ├── aceticacid.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── quantumpioneer_solvation_dataset_open_shell_species/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── quantumpioneer_solvation_dataset_reactions/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── quantumpioneer_solvation_dataset_transition_states/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   └── ...
│   ├── b/
│   └── ...
└── README.md
```

Within each top-level category the files are organized into subdirectories named after
the first alphabetical character of the solvent name (e.g. `a/`, `b/`, …). Each CSV
file is named `<solvent_name>.csv`, where `<solvent_name>` is the COSMO-RS solvent
identifier.
