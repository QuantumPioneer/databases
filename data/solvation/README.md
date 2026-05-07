# Solvation Data

Computed solvation free energies and enthalpies at 298.15 K for solute–solvent pairs, generated
by the COSMO-RS-based workflow described in the QuantumPioneer project paper. Each CSV file
corresponds to a single solvent (295 solvents total) and contains solvation properties for
every solute evaluated in that solvent.

## Dataset Schemas

### Closed-Shell Species, Open-Shell Species

| Column             | Description                                                     |
|--------------------|-----------------------------------------------------------------|
| `smiles`           | Canonical SMILES of the solute                                  |
| `Gsolv (kcal/mol)` | Solvation free energy of the solute in this solvent at 298.15 K |
| `Hsolv (kcal/mol)` | Solvation enthalpy of the solute in this solvent at 298.15 K    |

**Note:** The transition states are represented as reaction SMILES (`r1.r2>>p1.p2`).

### Reactions

| Column                       | Description                                                                |
|------------------------------|----------------------------------------------------------------------------|
| `rxn_smiles`                 | Reaction SMILES (`r1.r2>>p1.p2`)                                           |
| `DDGsolv_forward (kcal/mol)` | Solvation free energy of activation in the forward direction (`r1.r2>>ts`) |
| `DDGsolv_reverse (kcal/mol)` | Solvation free energy of activation in the reverse direction (`p1.p2>>ts`) |
| `DDHsolv_forward (kcal/mol)` | Solvation enthalpy of activation in the forward direction (`r1.r2>>ts`)    |
| `DDHsolv_reverse (kcal/mol)` | Solvation enthalpy of activation in the reverse direction (`p1.p2>>ts`)    |

All energies are in kcal/mol.

## Directory Structure

```
data/solvation/
├── closed_shell_species/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   ├── aceticacid.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── open_shell_species/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── reactions/
│   ├── a/
│   │   ├── acetaldehyde.csv
│   │   └── ...
│   ├── b/
│   └── ...
├── transition_states/
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
