import os
import pathlib
from pymol import cmd

def extract_binding_pocket(pdb_path, ref_ligand_resn, radius=6.0, outdir="data"):
    """
    Extracts a binding pocket around a reference ligand from a PDB structure using PyMOL.
    
    Args:
        pdb_path (str or Path): Path to the PDB file (downloaded structure)
        ref_ligand_resn (str): Residue name of the ligand (e.g. 'LIG', 'UNK', 'BNZ')
        radius (float): Radius in Å to define pocket size around ligand
        outdir (str or Path): Output folder to save extracted pocket
        
    Returns:
        str: Path to saved pocket PDB file
    """
    pdb_path = pathlib.Path(pdb_path)
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Load the structure
    cmd.reinitialize()
    cmd.load(str(pdb_path), "protein")

    # Select the ligand by residue name
    selection = f"resn {ref_ligand_resn}"
    if cmd.count_atoms(selection) == 0:
        raise ValueError(f"No atoms found for ligand residue '{ref_ligand_resn}' in {pdb_path.name}")

    # Define pocket: residues within radius Å of ligand
    pocket_sel = f"(br. ({selection} expand {radius}))"
    cmd.select("pocket", pocket_sel)

    # Save pocket
    pocket_filename = pdb_path.stem + f"_pocket_{ref_ligand_resn}.pdb"
    pocket_path = f"{outdir}/pockets/{pocket_filename}"
    cmd.save(str(pocket_path), "pocket")
    print(f"Saved pocket around {ref_ligand_resn} (radius={radius}Å) to {pocket_path}")

    # Clean up
    cmd.delete("all")
    return str(pocket_path)
