#!/bin/bash

#SBATCH --job-name=data_joining
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=2:00:00
#SBATCH --array=0-1000
#SBATCH --output=/labs/mpsnyder/LongCovidEkanath/output/data_joining/print_output/%A_%a.out
#SBATCH --error=/labs/mpsnyder/LongCovidEkanath/output/data_joining/error/%A_%a.err

module load miniconda/3
python3 data_joining.py $SLURM_ARRAY_TASK_ID