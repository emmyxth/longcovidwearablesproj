#!/bin/bash

#SBATCH --job-name=patient_RHR_process
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=1:00:00
#SBATCH --array=0-100
#SBATCH --output=/labs/mpsnyder/long-covid-study-data/output/RHR_process_%A_%a.out
#SBATCH --error=/labs/mpsnyder/long-covid-study-data/output/RHR_process_%A_%a.err

module load miniconda/3
FILES=(/labs/mpsnyder/long-covid-study-data/final_data/*)
python3 RHR.py ${FILES[$SLURM_ARRAY_TASK_ID]}