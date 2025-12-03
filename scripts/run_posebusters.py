from rdkit import Chem
from posebusters import PoseBusters

outdir = "../data/posebusters_results.csv"

# Replace with your SDF file path
gen_ligands_sdf_file = "../data/generated_ligands/generated_ligands.sdf"

# Create a supplier (generator) of RDKit Mol objects
supplier = Chem.SDMolSupplier(gen_ligands_sdf_file, removeHs=False)  # keep hydrogens if you want

# Convert to a list
gen_ligand_mols = [mol for mol in supplier if mol is not None]
print(f"Loaded {len(gen_ligand_mols)} molecules")

# load reference ligand, convert to rdkit mol
ref_ligand_sdf_file = "../data/pockets/mrgx4_human_8K4S_ligand_JW0.sdf"
supplier = Chem.SDMolSupplier(ref_ligand_sdf_file, removeHs=False)  # keep hydrogens if you want
ref_ligand_mol = supplier[0]

print("Reference ligand loaded")

# do with posebusters
buster = PoseBusters(config="mol")
# df = buster.bust([gen_ligands_sdf_file], ref_ligand_sdf_file, None, full_report=True)
df = buster.bust(gen_ligand_mols, ref_ligand_mol, None, full_report=True)

df.to_csv(outdir, index=False)


# load pocket as rdkit mol- do later

