import os
import subprocess
from pathlib import Path

def run_drugflow(pocket_pdb, ligand_sdf, outdir="data/generated_ligands", num_ligands=50, device="cpu"):
    """
    Runs DrugFlow to generate de novo ligands for a protein pocket.

    Args:
        pocket_pdb (str): Path to the protein pocket PDB file.
        ligand_sdf (str): Path to the reference ligand SDF file.
        outdir (str): Output directory for generated ligands.
        num_ligands (int): Number of ligands to generate.
        device (str): 'cpu' or 'cuda' (if you have a GPU).

    Returns:
        str: Path to the generated ligand directory.
    """

    pocket_pdb = Path(pocket_pdb).resolve()
    ligand_sdf = Path(ligand_sdf).resolve()
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    drugflow_path = Path(__file__).parents[1] / "externals" / "drugflow"
    run_script = drugflow_path / "scripts" / "generate.py"  # main entry point in DrugFlow repo

    if not run_script.exists():
        raise FileNotFoundError(f"Could not find generate.py at {run_script}")

    cmd = [
        "python", str(run_script),
        "--pocket", str(pocket_pdb),
        "--ref_ligand", str(ligand_sdf),
        "--num_samples", str(num_ligands),
        "--device", device,
        "--output", str(outdir)
    ]

    print(f"Running DrugFlow to generate {num_ligands} ligands...")
    subprocess.run(cmd, check=True)
    print(f"Ligands saved to: {outdir}")

    return str(outdir)


if __name__ == "__main__":
    run_drugflow(
        pocket_pdb="data/pockets/8K4S_pocket_LIG.pdb",
        ligand_sdf="data/pockets/8K4S_ligand_LIG.sdf",
        outdir="data/generated_ligands/8K4S",
        num_ligands=50,
        device="cpu"
    )
