# Description
This folder is used to consolidate each type of wearable data of each participant into a single csv file for easy plotting and statistical analysis.

The raw data paths are:
```
COVID_STUDY_PATH = "/labs/mpsnyder/long-covid-study-data/raw_data/COVID_GCB/covid-study/"
LONG_COVID_STUDY_PATH = "/labs/mpsnyder/long-covid-study-data/raw_data/longcovid2022-study/longcovid2022-processed/"
SCG_FOLDER_PATH = "/labs/mpsnyder/long-covid-study-data/raw_data/LongCOVIDSCG/"
```
The output files are in:
```
OUTPUT_FOLDER_PATH = "/labs/mpsnyder/LongCovidEkanath/final_data_recleaned/"
```
These paths are defined as constants in `data_joining.py`. We can change these paths to point to the updated location if needed.

# Usage
To run the script, run the following command:
```
python3 data_joining.py <index>
```
where `<index>` is the index of the participant you want to join the data for. The index corresponds to the order in the ID mapping document.

We can also run the script for all participants by submitting the job to the Slurm job scheduler with the bash script `data_joining.sh`. To do this, run the following command:
```
sbatch data_joining.sh
```
You can check the status of the job with the following command:
```
sacct -n -X -j <jobid>
```
where `<jobid>` is the id of the current job, which you will get when you submit the job. If the job is in the queue, you can cancel the job with the following command:
```
scancel <job_id>
```
where `<job_id>` is the job id of the job you want to cancel. 

The output of the job is written to the folder 
```
/labs/mpsnyder/LongCovidEkanath/output/data_joining/print_output
```
and the error of the data is written to the folder
```
/labs/mpsnyder/LongCovidEkanath/output/data_joining/error
```

# Cleaning Steps
The following steps are performed to clean the data:
1. Throw away any invalid data (e.g. files with no data, files with error messages, etc.)
2. Ensure that every file has the same column names in the same order: `Device, Start_Date, End_Date, Start_Time, End_Time, Value, Tag, Type`
3. Ensure that every file has the same data type for each column: 
    - `Device`: string
    - `Start_Date`: YYYY-MM-DD
    - `End_Date`: YYYY-MM-DD | NaN
    - `Start_Time`: HH:MM:SS | NaN
    - `End_Time`: HH:MM:SS | NaN
    - `Value`: float | NaN (sleep SL data does not have a value)
    - `Tag`: string | NaN
    - `Type`: string | NaN (only for sleep SL data; "Asleep" or "InBed")

# Note
The script only cleans the HR, ST, and SL data. Other data types (e.g. resHeart etc.) are not cleaned and are not put into the output folder.