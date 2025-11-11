import yaml
import pathlib
from scripts.download_structure import download_gpcrdb_structure
from scripts.extract_pocket import extract_binding_pocket


def main():

    print('hello')

    with open('configs/config.yaml', 'r') as f:
        cfg = yaml.safe_load(f)

    pdb_id = cfg["structure"]["pdb_id"]
    outdir = cfg["structure"]["outdir"]

    pdb_path = download_gpcrdb_structure(pdb_id, outdir)

    print(f"Structure saved at: {pdb_path}")

    # extract pocket
    




if __name__ == "__main__":
    main()