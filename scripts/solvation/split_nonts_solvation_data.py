# %%
import pathlib

import pandas as pd
import swifter

from rdkit import Chem
from rdkit.Chem import Descriptors
from tqdm.auto import tqdm

# %%
DATA_DIR = pathlib.Path("/home/shared/projects/quantum_green/datasets_for_publication/data/solvation")
QUANTUM_GREEN_DIR = pathlib.Path("/home/shared/projects/quantum_green")
PAPER_DATA_DIR = QUANTUM_GREEN_DIR / "paper" / "data"

# %%
def molecule_from_smiles(smiles, remove_atom_mapping=False):
    mol = Chem.MolFromSmiles(smiles)
    if remove_atom_mapping:
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(0)
    return mol


def canonical_smiles_from_molecule(mol, isomeric=True):
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
    lambda x: canonical_smiles_from_molecule(molecule_from_smiles(x), isomeric=False)
)
(names_df["smiles"] != non_isomeric_canonical_smiles).sum()

# %%
smiles_to_name_mapping = names_df.set_index("smiles")["cosmo_name"].to_dict()

# %% [markdown]
# ## Species Data

# %%
data = pd.read_csv(
    PAPER_DATA_DIR / "solvation" / "FILTERED_DEDUPLICATED_full_data_v3.csv",
    low_memory=False,
)
head(data)

# %%
unique_solvents = pd.DataFrame(data["solvent_smiles"].unique(), columns=["solvent_smiles"])
unique_solvents["non_isomeric_canonical_smiles"] = unique_solvents["solvent_smiles"].apply(
    lambda x: canonical_smiles_from_molecule(molecule_from_smiles(x), isomeric=False)
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
unique_solutes = pd.DataFrame(
    data["solute_smiles"].unique(), columns=["atom_mapped_smiles"]
)
head(unique_solutes)

# %%
molecules = swifter_apply(
    unique_solutes["atom_mapped_smiles"],
    lambda x: molecule_from_smiles(x, remove_atom_mapping=True),
    desc="Generating mols",
)

unique_solutes["canonical_smiles"] = swifter_apply(
    molecules,
    Chem.MolToSmiles,
    desc="Generating canonical smiles",
)

unique_solutes["num_radical_electrons"] = swifter_apply(
    molecules,
    Descriptors.NumRadicalElectrons,
    desc="Detecting radical electrons",
)

head(unique_solutes)

# %%
solute_to_canonical_smiles_mapping = unique_solutes.set_index(
    "atom_mapped_smiles"
)["canonical_smiles"].to_dict()

solute_to_num_radical_electrons_mapping = unique_solutes.set_index(
    "atom_mapped_smiles"
)["num_radical_electrons"].to_dict()

# %%
data["smiles"] = data["solute_smiles"].map(solute_to_canonical_smiles_mapping.get)
data["num_radical_electrons"] = data["solute_smiles"].map(solute_to_num_radical_electrons_mapping)
head(data)

# %%
ouput_columns = ["smiles", "Gsolv (kcal/mol)", "Hsolv (kcal/mol)"]

# %%
grouped_solvents = data.groupby(["solvent_name", "num_radical_electrons"])

# %%
dirnames = {
    0: "closed_shell_species",
    1: "open_shell_species",
}
for dirname in dirnames.values():
    (DATA_DIR / dirname).mkdir(parents=True, exist_ok=True)

for (name, num_radical_electrons), group in tqdm(grouped_solvents, total=2*len(unique_solvents)):
    subdir = DATA_DIR / dirnames[num_radical_electrons] / first_letter(name)
    subdir.mkdir(parents=True, exist_ok=True)
    filename = f"{name}.csv"
    group[ouput_columns].to_csv(subdir / filename, index=False, float_format="%.10g")
