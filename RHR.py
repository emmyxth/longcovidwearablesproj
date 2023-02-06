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

def extract_rhr_fitbit(df_hr: pd.DataFrame, df_st: pd.DataFrame):
    # check if it has enough columns to compute 
    if not helper.check_runnable(df_hr, df_st, "Fitbit"):  return helper.create_df([[],[],[],[]])
    # columns to fill. Those columns have source, ensured by the above function 
    device_col, start_date_col, start_time_col, value_col = [], [], [], []
    columns = [device_col, start_date_col, start_time_col, value_col]
    
    # get converted datetime obj for both hr and st data 
    
    hr_i, st_i = 0, 0
    while hr_i < len(df_hr.Start_Time) and st_i < len(df_st.Start_Time):
        # get updated datetime
        hr_datetime, st_datetime = helper.get_datetime(df_hr, hr_i), helper.get_datetime(df_st, st_i)
        
        while (hr_datetime < st_datetime):
            print(hr_datetime, st_datetime)
            # it is RHR 
            columns = helper.fill_columns(hr_i, columns, df_hr)
            hr_i += 1
            if hr_i >= len(df_hr.Start_Time):  break
            hr_datetime = helper.get_datetime(df_hr, hr_i)
        
        if hr_i >= len(df_hr.Start_Time) or st_i >= len(df_st.Start_Time):  break  
        
        # hr_datetime must be greater than st_datetime, but not nec abt hr_datetime[hr_i] - 10 min 
        while (hr_datetime >= st_datetime):
            print(hr_datetime, st_datetime)
            # in between 
            if (hr_datetime - timedelta(minutes=10) <= st_datetime) and (st_datetime <= hr_datetime):
                # not rhr 
                hr_i += 1
                if hr_i >= len(df_hr.Start_Time):  break
                hr_datetime = helper.get_datetime(df_hr, hr_i)
            else:
                st_i += 1
                if st_i >= len(df_st.Start_Time):  break
                st_datetime = helper.get_datetime(df_st, st_i)
              
    while hr_i < len(df_hr.Start_Time):
        # yes rhr
        columns = helper.fill_columns(hr_i, columns, df_hr) 
        hr_i += 1
        if hr_i >= len(df_hr.Start_Time):  break
        hr_datetime = helper.get_datetime(df_hr, hr_i)
            
    df = helper.create_df(columns)
    
    return df      


def extract_rhr_applewatch(df_hr: pd.DataFrame, df_st: pd.DataFrame):
    # check if it has enough columns to compute 
    if not helper.check_runnable(df_hr, df_st, "Apple Watch"):  return helper.create_df([[],[],[],[]])
    # columns to fill. Those columns have source, ensured by the above function 
    device_col, start_date_col, start_time_col, value_col = [], [], [], []
    columns = [device_col, start_date_col, start_time_col, value_col]
    
    hr_i, st_i = 0, 0
    while hr_i < len(df_hr.Start_Time) and st_i < len(df_st.Start_Time):
        
        hr_datetime = helper.get_datetime_applewatch(df_hr, hr_i, "Start")
        st_start_time, st_end_time = helper.get_datetime_applewatch(df_st, st_i, "Start"), helper.get_datetime_applewatch(df_st, st_i, "End")
        
        # while hr_datetime < st_start, all RHR
        while (hr_datetime < st_start_time):
            columns = helper.fill_columns(hr_i, columns, df_hr)
            hr_i += 1
            if hr_i >= len(df_hr.Start_Date):  break 
            hr_datetime = helper.get_datetime_applewatch(df_hr, hr_i, "Start")
#             print("success")
            
        if hr_i >= len(df_hr.Start_Time) or st_i >= len(df_st.Start_Time):  break 
            
        # now, hr_datetime >= st_start_time must hold true 
        # loop while hr_datetime > st_datetime_start
        while (hr_datetime >= st_start_time):
            # case 1: st_start <= hr_time <= st_end, then not RHR
            # case 2: st_end < hr_time, but hr_time - 10 min <= st_end
            if ((st_start_time <= hr_datetime and hr_datetime <= st_end_time) or 
               hr_datetime - timedelta(minutes=10) <= st_end_time):
                hr_i += 1
                if hr_i >= len(df_hr.Start_Date):  break
                hr_datetime = helper.get_datetime_applewatch(df_hr, hr_i, "Start")
            else:
                st_i += 1
                if st_i >= len(df_st.Start_Date):  break 
                st_start_time, st_end_time = helper.get_datetime_applewatch(df_st, st_i, "Start"), helper.get_datetime_applewatch(df_st, st_i, "End")
        
        if hr_i >= len(df_hr.Start_Time) or st_i >= len(df_st.Start_Time):  break 

    while hr_i < len(df_hr.Start_Time):
        columns = helper.fill_columns(hr_i, columns, df_hr)
        hr_i += 1
        if hr_i >= len(df_hr.Start_Date):  break
        hr_datetime = helper.get_datetime_applewatch(df_hr, hr_i, "Start")
    
    df = helper.create_df(columns)
    return df



###### TO DO ########
if __name__ == "__main__":
    #### EDIT HERE, DEPENDING ON HOW BASH SCRIPT USES THIS .py FILE ####
    # if command line format is: RHR.py [participant_id], then:
    participant_id = os.path.basename(sys.argv[1])
    print("participant_id: ", participant_id)

    ### EDIT THE ABOVE IF DIFFERNT FORMAT ### 

    extract_rhr(participant_id)
    print("Done extracting RHR for participant: ", participant_id)