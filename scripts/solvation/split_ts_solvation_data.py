# %%
import pathlib

import pandas as pd
import swifter

from rdkit import Chem
from tqdm.auto import tqdm

# %%
DATA_DIR = pathlib.Path("/home/shared/projects/quantum_green/datasets_for_publication/data/solvation")
QUANTUM_GREEN_DIR = pathlib.Path("/home/shared/projects/quantum_green")
PAPER_DATA_DIR = QUANTUM_GREEN_DIR / "paper" / "data"

# %%
def canonical_smiles(smiles, isomeric=True, remove_atom_mapping=False):
    mol = Chem.MolFromSmiles(smiles)
    if remove_atom_mapping:
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(0)
    return Chem.MolToSmiles(mol, isomericSmiles=isomeric)


def first_letter(name):
    return next(s for s in name if s.isalpha())


pd.set_option('display.max_columns', None)


def head(df, n=2):
    display(df.head(n))
    print(f"Contains {len(df)} rows")
    
    
def swifter_apply(series, func, desc=None):
    if desc is None:
        desc = "Applying function"
    return series.swifter.progress_bar(True, desc).apply(func)

# %%
names_df = pd.read_csv(pathlib.Path.cwd() / "solvents.csv")
head(names_df)

# %%
non_isomeric_canonical_smiles = names_df["smiles"].apply(
    lambda x: canonical_smiles(x, isomeric=False)
)
(names_df["smiles"] != non_isomeric_canonical_smiles).sum()

# %%
smiles_to_name_mapping = names_df.set_index("smiles")["cosmo_name"].to_dict()

# %% [markdown]
# ## Transition State Data

# %%
data = pd.read_csv(
    PAPER_DATA_DIR / "ts_solvation" / "FINAL_dG_solv_pruned_nov17_with_reactant_product_dGsolv.csv",
)
head(data)

# %%
unique_solvents = pd.DataFrame(data["solvent_smiles"].unique(), columns=["solvent_smiles"])
unique_solvents["non_isomeric_canonical_smiles"] = unique_solvents["solvent_smiles"].apply(
    lambda x: canonical_smiles(x, isomeric=False)
)
head(unique_solvents)

# %%
(unique_solvents["solvent_smiles"] != unique_solvents["non_isomeric_canonical_smiles"]).sum()

# %%
solvent_smiles_to_non_isomeric_canonical_smiles_mapping = unique_solvents.set_index(
    "solvent_smiles"
)["non_isomeric_canonical_smiles"].to_dict()

solvent_smiles_to_name_mapping = {
    k: smiles_to_name_mapping[v]
    for k, v in solvent_smiles_to_non_isomeric_canonical_smiles_mapping.items()
}

# %%
data["solvent_name"] = data["solvent_smiles"].map(solvent_smiles_to_name_mapping)
head(data)

# %%
unique_reactants = pd.DataFrame(
    set().union(*[data[col] for col in ["r1", "r2", "p1", "p2"]]),
    columns=["atom_mapped_smiles"],
)
head(unique_reactants)

# %%
unique_reactants["canonical_smiles"] = swifter_apply(
    unique_reactants["atom_mapped_smiles"],
    lambda x: canonical_smiles(x, remove_atom_mapping=True),
    "Generating canonical smiles",
)
head(unique_reactants)

# %%
species_to_canonical_smiles_mapping = unique_reactants.set_index(
    "atom_mapped_smiles"
)["canonical_smiles"].to_dict()

# %%
for col in ["r1", "r2", "p1", "p2"]:
    data[col + "_smiles"] = swifter_apply(
        data[col],
        lambda x: species_to_canonical_smiles_mapping.get(x),
        f"Mapping {col}",
    )
head(data)

# %%
data["rxn_smiles"] = (
    data["r1_smiles"]
    + "."
    + data["r2_smiles"]
    + ">>"
    + data["p1_smiles"]
    + "."
    + data["p2_smiles"]
)
head(data)

# %%
ouput_columns = [
    "rxn_smiles",
    "Gsolv (kcal/mol)",
    "r1_Gsolv",
    "r2_Gsolv",
    "p1_Gsolv",
    "p2_Gsolv",
    "DDGsolv_forward (kcal/mol)",
    "DDGsolv_reverse (kcal/mol)",
    "Hsolv (kcal/mol)",
    "r1_Hsolv",
    "r2_Hsolv",
    "p1_Hsolv",
    "p2_Hsolv",
    "DDHsolv_forward (kcal/mol)",
    "DDHsolv_reverse (kcal/mol)",
]

# %%
grouped_solvents = data.groupby("solvent_name")

# %%
DIR = DATA_DIR / "transition_states"
DIR.mkdir(parents=True, exist_ok=True)
for name, group in tqdm(grouped_solvents, total=len(unique_solvents)):
    subdir = DIR / first_letter(name)
    subdir.mkdir(parents=True, exist_ok=True)
    group[ouput_columns].to_csv(subdir / f"{name}.csv", index=False, float_format="%.10g")
