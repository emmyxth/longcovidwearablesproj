import os 
import pandas as pd
import glob 
import numpy as np
from datetime import datetime, timedelta

start_path = "/labs/mpsnyder/long-covid-study-data/final_data"
dst_path = "/labs/mpsnyder/long-covid-study-data/final_data_cleaned"
os.chdir(start_path)

participants_id = glob.glob('*')
part_ids = participants_id[:100]
one_id = participants_id[16]

# process corresponding csv file
def clean_csvs(participant_id: str):
    # useful paths and column names
    full_path_dir = os.path.join(start_path, participant_id)
    full_path_hr = os.path.join(start_path, participant_id, "hr.csv")
    full_path_st = os.path.join(start_path, participant_id , "st.csv")
    full_path_dst = os.path.join(dst_path, participant_id)
    column_names = ['Device','Start_Date','End_Date','Start_Time','End_Time','Value','Tag','Type']

    # create directory if it doesn't exist
    if os.path.exists(full_path_hr) and os.path.exists(full_path_st) and not os.path.exists(full_path_dir):
        os.mkdir(full_path_dir)

    df_hr_new = pd.DataFrame(columns=column_names)
    df_st_new = pd.DataFrame(columns=column_names)

    # clean hr csv file and save it to the directory
    if os.path.exists(full_path_hr):
        df_hr = pd.read_csv(full_path_hr)

        for column_name in column_names:
            df_hr_new[column_name] = df_hr[column_name]
        last_row = df_hr_new.iloc[-1]["Value"]

        # remove last row if value is not a number
        if not str(last_row).isdigit():
            df_hr_new = df_hr_new[:-1]

            # save to the new destination
        df_hr_new.to_csv(os.path.join(full_path_dst, "hr.csv"), index=False)
    
    # clean st csv file and save it to the directory
    if os.path.exists(full_path_st):
        df_st = pd.read_csv(full_path_st)

        for column_name in column_names:
            df_st_new[column_name] = df_st[column_name]
        
        # remove last row if value is not a number
        last_row = df_st_new.iloc[-1]["Value"]
        if not str(last_row).isdigit():
            df_st_new = df_st_new[:-1]
        
        # save to the new destination
        df_st_new.to_csv(os.path.join(full_path_dst, "hr.csv"), index=False)