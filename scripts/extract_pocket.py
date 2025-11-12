import os
import pathlib
from pymol import cmd
from rdkit import Chem


def extract_binding_pocket(pdb_path, ref_ligand_resn, radius=6.0, outdir="data"):
    """
    Extracts a binding pocket around a reference ligand from a PDB structure using PyMOL,
    and saves both the pocket (PDB) and ligand (PDB/SDF if possible).

    Args:
        pdb_path (str or Path): Path to the PDB file (downloaded structure)
        ref_ligand_resn (str): Residue name of the ligand (e.g. 'LIG', 'UNK', 'BNZ')
        radius (float): Radius in Å to define pocket size around ligand
        outdir (str or Path): Output folder to save extracted pocket/ligand

    Returns:
        dict: Paths to saved files (pocket_pdb, ligand_pdb, ligand_sdf)
    """

    pdb_path = pathlib.Path(pdb_path)
    outdir = pathlib.Path(f"{outdir}/pockets")
    outdir.mkdir(parents=True, exist_ok=True)

    # Load structure
    cmd.reinitialize()
    cmd.load(str(pdb_path), "protein")

    # Select ligand by residue name
    ligand_sel = f"resn {ref_ligand_resn}"
    if cmd.count_atoms(ligand_sel) == 0:
        raise ValueError(f"No atoms found for ligand residue '{ref_ligand_resn}' in {pdb_path.name}")

    # Save ligand separately
    ligand_filename = pdb_path.stem + f"_ligand_{ref_ligand_resn}.pdb"
    ligand_path = outdir / ligand_filename
    cmd.save(str(ligand_path), ligand_sel)
    print(f"Saved ligand {ref_ligand_resn} to {ligand_path}")

    # Define and save pocket (residues within radius Å of ligand)
    pocket_sel = f"(br. ({ligand_sel} expand {radius}))"
    cmd.select("pocket", pocket_sel)

    pocket_filename = pdb_path.stem + f"_pocket_{ref_ligand_resn}.pdb"
    pocket_path = outdir / pocket_filename
    cmd.save(str(pocket_path), "pocket")
    print(f"Saved pocket (radius={radius}Å) to {pocket_path}")

    # convert ligand PDB to SDF using RDKit
    ligand = Chem.MolFromPDBFile(str(ligand_path), removeHs=False)
    ligand_sdf_path = ligand_path.with_suffix(".sdf")
    Chem.MolToMolFile(ligand, str(ligand_sdf_path))
    
    print(f"Exported ligand SDF to {ligand_sdf_path}")


    # Cleanup
    cmd.delete("all")

    return str(pocket_path)
