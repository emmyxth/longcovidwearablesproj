#!/bin/bash

#SBATCH --job-name=patient_RHR_process
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=1:00:00
#SBATCH --array=0-9
#SBATCH --output=./output/patient_RHR_process_%A_%a.out
#SBATCH --error=./output/patient_RHR_process_%A_%a.err

if [ $# -ne 2 ]; then
    echo "Usage: $0 <small|large> <linear|majority>"
    exit 1
fi

module load miniconda/3
FILES=(/labs/mpsnyder/long-covid-study-data/final_data/*)
python3 setup_data.py $1 $2 ${FILES[$SLURM_ARRAY_TASK_ID]} $SLURM_ARRAY_TASK_ID