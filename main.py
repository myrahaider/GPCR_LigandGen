import yaml
import pathlib
from scripts.download_structure import download_gpcrdb_structure
from scripts.extract_pocket import extract_binding_pocket
from scripts.run_drugflow import run_drugflow


def main():

    with open('configs/config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    pdb_id = cfg["pdb_id"]
    outdir = cfg["outdir"]
    pdb_path = cfg["pdb_file"]

    #pdb_path = download_gpcrdb_structure(pdb_id, outdir)

    print(f"Structure saved at: {pdb_path}")

    ref_ligand_resn = cfg["residue_name"]
    radius = cfg["pocket_radius"]

    #pocket_path, ligand_sdf_path = extract_binding_pocket(pdb_path, ref_ligand_resn, radius, outdir)

    pocket_path = "data/pockets/mrgx4_human_8K4S_pocket_JW0.pdb"
    ligand_sdf_path = "data/pockets/mrgx4_human_8K4S_ligand_JW0.sdf"

    print(f"Pocket saved at: {pocket_path}")
    print(f"Ligand SDF saved at: {ligand_sdf_path}")

    num_ligands = cfg["num_ligands"]
    device = cfg["device"]
    
    generated_ligands_dir = run_drugflow(pocket_path, ligand_sdf_path, outdir, num_ligands, device)


    
if __name__ == "__main__":
    main()