import yaml
import pathlib
from scripts.download_structure import download_gpcrdb_structure
from scripts.extract_pocket import extract_binding_pocket


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

    pocket_path = extract_binding_pocket(pdb_path, ref_ligand_resn, radius, outdir)







if __name__ == "__main__":
    main()