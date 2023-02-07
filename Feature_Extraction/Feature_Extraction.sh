#!/bin/bash

#SBATCH --job-name=patient_feature_extraction
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=interactive
#SBATCH --account=default
#SBATCH --time=2:00:00
#SBATCH --array=2500-5572
#SBATCH --output=/labs/mpsnyder/long-covid-study-data/output/patient_feature_extraction/%A_%a.out
#SBATCH --error=/labs/mpsnyder/long-covid-study-data/output/patient_feature_extraction/%A_%a.err

module load miniconda/3
FILES=(/labs/mpsnyder/long-covid-study-data/final_data/*)
python3 LongCOVID_Feature_Extraction.py ${FILES[$SLURM_ARRAY_TASK_ID]}