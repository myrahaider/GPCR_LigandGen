import os
import subprocess
from pathlib import Path
import sys

def run_drugflow(pocket_pdb, ligand_sdf, outdir="data", num_ligands=50, device="cpu"):
    """
    Runs DrugFlow to generate de novo ligands for a given protein pocket

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
    run_script = drugflow_path / "src" / "generate.py" 
    checkpoint_path = drugflow_path / "checkpoints" / "drugflow.ckpt"

    if not run_script.exists():
        raise FileNotFoundError(f"Could not find generate.py at {run_script}")

    cmd = [
        sys.executable, str(run_script),
        "--protein", str(pocket_pdb),
        "--ref_ligand", str(ligand_sdf),
        "--checkpoint", str(checkpoint_path),
        "--n_samples", str(num_ligands),
        "--device", str(device),
        "--metrics_output", str(outdir / "metrics" / "metrics.csv"),
        "--output", str(outdir / "generated_ligands" / "generated_ligands.sdf")
    ]

    print(f"Running DrugFlow to generate {num_ligands} ligands...")
    subprocess.run(cmd, check=True)
    print(f"Ligands saved to: {outdir}")

    return str(outdir)
