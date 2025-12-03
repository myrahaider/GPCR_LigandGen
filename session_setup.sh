#!/bin/bash

# Load modules
module load anaconda3/2024.10-1
module load cuda/12.4.0
module load gcc/13.3.1-p20240614

# activate conda environment
conda activate drugflow

# Fix RDKit library issue
export LD_PRELOAD=$CONDA_PREFIX/lib/libstdc++.so.6
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH