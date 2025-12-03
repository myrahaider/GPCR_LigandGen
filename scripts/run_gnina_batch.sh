#!/bin/bash

receptor="data/pdbqt_files/receptor.pdbqt"
ref_lig="data/pdbqt_files/ref_ligand.pdbqt"
lig_dir="data/pdbqt_files"
out_dir="data/gnina_output"

mkdir -p "$out_dir"

csv_out="${out_dir}/gnina_summary.csv"

# Write CSV header
echo "ligand,vina_affinity,cnn_pose_score,cnn_affinity" > "$csv_out"

for i in $(seq 1 64); do
    lig="${lig_dir}/ligand_${i}.pdbqt"
    sdf_out="${out_dir}/ligand_${i}_docked.sdf"
    log_out="${out_dir}/ligand_${i}.log"

    echo "Docking ligand_${i}..."

    ./gnina \
        --receptor "$receptor" \
        --ligand "$lig" \
        --autobox_ligand "$ref_lig" \
        --out "$sdf_out" \
        --seed 0 \
        --log "$log_out"

    if [ $? -ne 0 ]; then
        echo "Error docking ligand_${i}"
        echo "ligand_${i},ERROR,ERROR,ERROR" >> "$csv_out"
        continue
    fi

    # Extract best-scoring mode from gnina log
    vina=$(grep -m1 -E "^[[:space:]]*[0-9]+[[:space:]]+-" "$log_out" | awk '{print $2}')
    cnn_score=$(grep -m1 -E "^[[:space:]]*[0-9]+[[:space:]]+-" "$log_out" | awk '{print $3}')
    cnn_aff=$(grep -m1 -E "^[[:space:]]*[0-9]+[[:space:]]+-" "$log_out" | awk '{print $4}')

    echo "ligand_${i},$vina,$cnn_score,$cnn_aff" >> "$csv_out"

    echo "Finished ligand_${i}"
done

echo "Done! Summary written to: $csv_out"

