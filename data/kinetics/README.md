# QuantumPioneer Kinetics Dataset

| Column             | Type   | Units       | Description                                        |
| ------------------ | ------ | ----------- | -------------------------------------------------- |
| **`rxn_smi`**      | string | —           | Reaction SMILES (`r1.r2>>p1.p2`)                   |
| **`k_298`**        | number | m³/(mol·s)  | Bimolecular rate coefficient at 298 K              |
| **`A_low`**        | number | m³/(mol·s)  | Arrhenius pre-exponential factor, 300–1000 K       |
| **`Ea_low`**       | number | kcal/mol    | Activation energy, 300–1000 K                      |
| **`A_high`**       | number | m³/(mol·s)  | Arrhenius pre-exponential factor, 1000–2000 K      |
| **`Ea_high`**      | number | kcal/mol    | Activation energy, 1000–2000 K                     |
| **`barrier`**      | number | kcal/mol    | Forward barrier (DLPNO + scaled DFT ZPE)           |
| **`Hrxn`**         | number | kcal/mol    | Forward reaction enthalpy (DLPNO + scaled DFT ZPE) |
| **`deltaHrxn298`** | number | kcal/mol    | Forward reaction enthalpy at 298 K                 |
| **`deltaGrxn298`** | number | kcal/mol    | Forward reaction Gibbs energy at 298 K             |
| **`P2M`**          | number | kcal/mol    | Petersson-to-Melius energy difference at 298 K     |

The thermodynamic properties `deltaHrxn298` and `deltaGrxn298` are derived from calculations using
Petersson-type bond additivity corrections (BACs). Add `P2M` to these to obtain their Melius-type
BAC-corrected versions.
