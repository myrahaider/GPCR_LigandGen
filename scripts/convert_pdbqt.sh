#!/bin/bash

input_dir="data/generated_ligands"
output_dir="data/pdbqt_files"

mkdir -p "$output_dir"

for i in $(seq 1 64); do
    input_file="${input_dir}/ligand_${i}.pdb"
    output_file="${output_dir}/ligand_${i}.pdbqt"

    echo "Converting $input_file → $output_file"

    obabel "$input_file" -O "$output_file" \
        --addhydrogens \
        --partialcharge gasteiger

    if [ $? -ne 0 ]; then
        echo "Error converting ligand_${i}.sdf"
    else
        echo "Done"
    fi
done