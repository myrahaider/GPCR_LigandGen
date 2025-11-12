import os
import pathlib
from pymol import cmd

def extract_binding_pocket(pdb_path, ref_ligand_resn, radius=6.0, outdir="data"):
    """
    Extracts a binding pocket around a reference ligand from a PDB structure using PyMOL.
    Saves both the cleaned protein pocket (ATOM only) and the isolated ligand (HETATM only).
    
    Args:
        pdb_path (str or Path): Path to the PDB file (downloaded structure)
        ref_ligand_resn (str): Residue name of the ligand (e.g. 'LIG', 'UNK', 'BNZ')
        radius (float): Radius in Å to define pocket size around ligand
        outdir (str or Path): Output folder to save extracted pocket and ligand
        
    Returns:
        tuple[str, str]: Paths to saved (pocket_path, ligand_path)
    """

    pdb_path = pathlib.Path(pdb_path)
    outdir = pathlib.Path(f"{outdir}/pockets")
    outdir.mkdir(parents=True, exist_ok=True)

    # Load the structure
    cmd.reinitialize()
    cmd.load(str(pdb_path), "protein")

    # Select ligand by residue name
    ligand_sel = f"resn {ref_ligand_resn}"
    if cmd.count_atoms(ligand_sel) == 0:
        raise ValueError(f"No atoms found for ligand residue '{ref_ligand_resn}' in {pdb_path.name}")

    # Define pocket: protein residues within radius Å of ligand
    cmd.select("pocket", f"polymer.protein within {radius} of ({ligand_sel})")

    # Define output paths
    pocket_filename = pdb_path.stem + f"_pocket_{ref_ligand_resn}.pdb"
    ligand_filename = pdb_path.stem + f"_ligand_{ref_ligand_resn}.pdb"
    pocket_path = outdir / pocket_filename
    ligand_path = outdir / ligand_filename

    # Save pocket (ATOM only) and ligand (HETATM only)
    cmd.save(str(pocket_path), "pocket and polymer.protein")
    cmd.save(str(ligand_path), f"{ligand_sel} and not polymer.protein")

    print(f"Saved pocket: {pocket_path}")
    print(f"Saved ligand: {ligand_path}")

    cmd.delete("all")
    
    return str(pocket_path)
