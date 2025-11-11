import os
import requests
import yaml

def download_gpcrdb_structure(pdb_id, outdir="data/"):

    os.makedirs(outdir, exist_ok=True)

    url = f"https://gpcrdb.org/services/structure/{pdb_id}/"
    filename = f"{pdb_id}.pdb"

    print(f"Downloading from {url} ...")
    response = requests.get(url)

    if response.status_code == 200:
        outfile = os.path.join(f"{outdir}/raw", filename)

        with open(outfile, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename} successfully to {outdir}")

        return outfile
    
    else:
        raise ValueError(f"Failed to download {pdb_id} (HTTP {response.status_code})")
