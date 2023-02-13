#!/bin/bash

#SBATCH --job-name=clean_data
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=2:00:00
#SBATCH --array=0-5572
#SBATCH --output=/labs/mpsnyder/long-covid-study-data/output/data_joining/%A_%a.out
#SBATCH --error=/labs/mpsnyder/long-covid-study-data/output/data_joining/%A_%a.err

module load miniconda/3
python3 clean_data.py $SLURM_ARRAY_TASK_ID