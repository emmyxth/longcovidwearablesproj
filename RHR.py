from datetime import datetime, timedelta 
import pandas as pd
import os 
import glob 
import sys
import RHR_helper as helper

"""
Main RHR function.

params: participant_id 

Description:
Given a participant_id, the function finds the hr and st files of the participant, and stores as two dataframes. 
(If one or both hr and st files are not found, returns None). Then, it calls either (1) fitbit extract function or
(2) apple watch extract function, and stores a csv file in the participant_id's folder. 
"""
def extract_rhr(participant_id: str) -> None:
    start_path = "/labs/mpsnyder/long-covid-study-data/final_data" 
    os.chdir(start_path)
    # find hr and st csv file and check if it exists
    csv_file_path_hr = glob.glob(start_path + "/" + participant_id + "/*hr.csv") # hr files 
    csv_file_path_st = glob.glob(start_path + "/" + participant_id + "/*st.csv") # st files
    if len(csv_file_path_hr) == 0 and len(csv_file_path_st) == 0:  return  # returns None if no hr/st file found
    # open csv file 
    df_hr = pd.read_csv(csv_file_path_hr[0])
    df_st = pd.read_csv(csv_file_path_st[0])

    if df_hr.Device[0] == "Fitbit":
        df = extract_rhr_fitbit(df_hr, df_st)
        df.to_csv(start_path + "/" + participant_id + "/rhr.csv")

    elif df_hr.Device[0] == "HK Apple Watch":
        df = extract_rhr_applewatch(df_hr, df_st)
        df.to_csv(start_path + "/" + participant_id + "/rhr.csv")

"""
params: 
df_hr -> hr dataframe 
df_st -> st dataframe 

returns -> rhr dataframe, with the same columns as hr/st dataframe 

Description: Removes outliers. Extracts RHR. 
Logic: 
hr_starttime is either (1) before st_starttime or (2) after st_starttime.
    (1) while hr_starttime < st_starttime, all HR has to be RHR 
    (2) if hr_starttime > st_starttime, then either: 
        (1) while st_starttime < hr_starttime - 10min, skip to next st_starttime 
        (2) if hr_starttime - 10 min <= st_datetime <= hr_starttime 
            not RHR 
        (3) if hr_starttime < st_starttime
            it is RHR 
    repeat 
"""
def extract_rhr_fitbit(df_hr: pd.DataFrame, df_st: pd.DataFrame) -> pd.DataFrame:
    # express each df.column as a list, where we will populate 
    device_col, start_date_col, start_time_col, value_col = [], [], [], []
    columns = [device_col, start_date_col, start_time_col, value_col]
    source_columns = [df_hr.Device, df_hr.Start_Date, df_hr.Start_Time, df_hr.Value]

    # get converted datetime obj for both hr and st data 
    hr_datetime = helper.get_datetime_list(df_hr, "Start")
    st_datetime = helper.get_datetime_list(df_st, "Start")
        
    hr_i, st_i = 0, 0
    while hr_i < len(df_hr.Start_Time) and st_i < len(df_st.Start_Time):
        
        # while hr_datetime is before st_datetime, all hr are RHR
        while (hr_datetime[hr_i] < st_datetime[st_i]):
            # it is RHR
            columns = helper.fill_columns(hr_i, columns, source_columns)
            hr_i += 1
            if hr_i >= len(df_hr.Start_Time):  break
        
        if hr_i >= len(hr_datetime) or st_i >= len(st_datetime):  break  
        
        # hr_datetime must be greater than st_datetime, but not nec abt hr_datetime[hr_i] - 10 min 
        while (hr_datetime[hr_i] >= st_datetime[st_i]):
            # in between 
            if (hr_datetime[hr_i] - timedelta(minutes=10) <= st_datetime[st_i]) and (st_datetime[st_i] <= hr_datetime[hr_i]):
                # not rhr 
                hr_i += 1 
                if hr_i >= len(df_hr.Start_Time):  break
            # hr_datetime[hr_i] - 10 min > st_datetime 
            else:
                st_i += 1
                if st_i >= len(st_datetime):  break
        
    while hr_i < len(hr_datetime):
        columns = helper.fill_columns(hr_i, columns, source_columns)
        hr_i += 1
        if hr_i >= len(hr_datetime):  break
    
    df = helper.create_df(columns)
    
    return df


def extract_rhr_applewatch(df_hr: pd.DataFrame, df_st: pd.DataFrame) -> pd.DataFrame:
    device_col, start_date_col, end_date_col, start_time_col, end_time_col, value_col, tag_col, type_col = [], [], [], [], [], [], [], []
    columns = [device_col, start_date_col, end_date_col, start_time_col, end_time_col, value_col, tag_col, type_col]
    source_columns = [df_hr.Device, df_hr.Start_Date, df_hr.End_Date, df_hr.Start_Time, df_hr.End_Time, df_hr.Value, df_hr.Tag, df_hr.Type]
    
    # get converted datetime obj for both hr and st data 
    hr_datetime = helper.get_datetime_list(df_hr, "Start")
    st_datetime_start = helper.get_datetime_list(df_st, "Start")
    st_datetime_end = helper.get_datetime_list(df_st, "End")
    
    hr_i, st_i = 0, 0
    while hr_i < len(df_hr.Start_Time) and st_i < len(df_st.Start_Time):
        
        # while hr_datetime < st_start, all RHR
        while (hr_datetime[hr_i] < st_datetime_start[st_i]):
            columns = helper.fill_columns_applewatch(hr_i, columns, source_columns)
            hr_i += 1
            if hr_i + 1 >= len(df_hr.Start_Time):  break
        
        if hr_i >= len(hr_datetime) or st_i >= len(df_st.Start_Time):  break  
        
        # now, hr_datetime >= st_start_time must hold true 
        # loop while hr_datetime > st_datetime_start
        while (hr_datetime[hr_i] >= st_datetime_start[st_i]):
            # case 1: st_start <= hr_time <= st_end, then not RHR
            # case 2: st_end < hr_time, but hr_time - 10 min <= st_end
            if ((st_datetime_start[st_i] <= hr_datetime[hr_i] and hr_datetime[hr_i] <= st_datetime_end[st_i]) or
                hr_datetime[hr_i] - timedelta(minutes=10) <= st_datetime_end[st_i]):
                hr_i += 1
                if hr_i >= len(hr_datetime):  break
            # case 3: st_end < hr_time & hr_time - 10 min <= st_end, but next st can cause 
            #         case 1 or case 2 
            else: 
                st_i += 1
                if st_i >= len(st_datetime_start):  break
        
        if hr_i >= len(hr_datetime) or st_i >= len(df_st.Start_Time):  break  
        
    while hr_i < len(hr_datetime):
        columns = helper.fill_columns_applewatch(hr_i, columns, source_columns)
        if hr_i + 1 >= len(hr_datetime):  break
        hr_i += 1

    df = helper.create_df(columns)
    
    return df



###### TO DO ########
if __name__ == "__main__":
    #### EDIT HERE, DEPENDING ON HOW BASH SCRIPT USES THIS .py FILE ####
    # if command line format is: RHR.py [participant_id], then:
    participant_id = sys.argv[1]
    ### EDIT THE ABOVE IF DIFFERNT FORMAT ### 

    extract_rhr(participant_id)