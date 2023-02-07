from datetime import datetime, timedelta 
import pandas as pd

"""
params: 
index -> index of df_hr that we are interested in 
columns -> 2-D list we are populating, where each sub-list corresponds to columns in df_hr
source_columns -> 2-D list, where each sub-list are columns of df_hr

returns: 
columns -> updated columns list, where new "row" has been appended 
"""
def fill_columns(index: int, columns: list, df: pd.DataFrame):
    if type(df.Value[index]) == str: 
        return columns 
    if df.Value[index] > 200 or df.Value[index] < 30:
        return columns 
    # device 
    columns[0].append(df.Device[index])
    columns[1].append(df.Start_Date[index])
    columns[2].append(df.Start_Time[index])
    columns[3].append(df.Value[index])
    
    return columns

# checks if it has enough columns to be runnable 
def check_runnable(df_hr, df_st, mode):
    hr_req_columns = ["Device", "Start_Date", "Start_Time", "Value"]
    for col in hr_req_columns:
        if col not in df_hr.columns:
            return False
    if mode == "Fitbit":
        st_req_columns = ["Device", "Start_Date", "Start_Time", "Value"]
        for col in st_req_columns:
            if col not in df_st.columns:
                return False
    elif mode == "Apple Watch":
        st_req_columns = ["Device", "Start_Date", "Start_Time", "Value", "End_Date", "End_Time"]
        for col in st_req_columns:
            if col not in df_st.columns:
                print("false")
                return False
    else:
        return False
    return True

def get_datetime(df: pd.DataFrame, index):
    str_date, str_time = str(df.Start_Date[index]), str(df.Start_Time[index])
    # if str_date is None or str_time is None: return  
    date = datetime.strptime(str_date, "%Y-%m-%d")
    time = datetime.strptime(str_time, "%H:%M:%S").time()
    date_time = datetime.combine(date, time)
    return date_time 

def get_datetime_applewatch(df: pd.DataFrame, index, mode):
    str_date, str_time = "", ""
    if mode == "Start":
        str_date, str_time = str(df.Start_Date[index]), str(df.Start_Time[index])
    else:
        str_date, str_time = str(df.End_Date[index]), str(df.End_Time[index])
        
    # if str_date is None or str_time is None: return  
    date = datetime.strptime(str_date, "%Y-%m-%d")
    time = datetime.strptime(str_time, "%H:%M:%S").time()
    date_time = datetime.combine(date, time)
    return date_time  


"""
params: 
columns -> updated columns list, where new "row" has been appended

returns -> pandas dataframe 
"""
def create_df(columns: list) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "Device": columns[0],
            "Start_Date": columns[1],
            "Start_Time": columns[2],
            "Value": columns[3],
        }
    )
    return df
