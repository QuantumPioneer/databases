# QuantumPioneer Kinetics Dataset

| Column        | Type   | Units       | Description                                      |
| ------------- | ------ | ----------- | ------------------------------------------------ |
| **`rxn_smi`** | string | —           | Reaction SMILES (`r1.r2>>p1.p2`)                 |
| **`k_298`**   | number | m³/(mol·s)  | Bimolecular rate coefficient at 298 K            |
| **`A_low`**   | number | m³/(mol·s)  | Arrhenius pre-exponential factor, 300–1000 K     |
| **`Ea_low`**  | number | J/mol       | Activation energy, 300–1000 K                    |
| **`A_high`**  | number | m³/(mol·s)  | Arrhenius pre-exponential factor, 1000–2000 K    |
| **`Ea_high`** | number | J/mol       | Activation energy, 1000–2000 K                   |
| **`barrier`** | number | kcal/mol    | Forward barrier (ZPE-scaled DLPNO/DFT)           |
| **`Hrxn`**    | number | kcal/mol    | Forward reaction enthalpy (ZPE-scaled DLPNO/DFT) |
