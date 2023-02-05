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
def fill_columns(index: int, columns: list, source_columns: list) -> list:
    if source_columns[3][index] >= 200 or source_columns[3][index] <= 30:  return columns
    for i in range(len(columns)):
        columns[i].append(source_columns[i][index])
    return columns

def fill_columns_applewatch(index: int, columns: list, source_columns: list) -> list:
    if source_columns[5][index] >= 200 or source_columns[5][index] <= 30:  return columns
    for i in range(len(columns)):
        columns[i].append(source_columns[i][index])
    return columns

"""
Description: The function converts str date, "%Y-%m-%d", and str time, "%H:%M:%S", to datetime object: "%Y-%m-%d %H:%M:%S"
params: df -> dataframe of EITHER hr.csv or st.csv 
index: index of df's column: e.g. index = 5 if we want to access the str date df.Start_date[index]
returns: converted & combined datetime of the form "%Y-%m-%d %H:%M:%S"
"""
def convert_datetime_to_datetime_obj(start_date_list, start_time_list, index):
    if index >= len(start_date_list): return 
    str_date, str_time = start_date_list[index], start_time_list[index]
    date = datetime.strptime(str_date, "%Y-%m-%d")
    time = datetime.strptime(str_time, "%H:%M:%S").time()
    date_time = datetime.combine(date, time)
    return date_time

"""
params:
df -> dataframe to get the string datetime
mode -> "Start" or "End"

returns:
datetime_res -> list of datetime objects. 

Description:
Use this function in the beginning of extract_rhr function to convert all 
str datetime to datetime object. 
"""
def get_datetime_list(df: pd.DataFrame, mode: str) -> list:
    datetime_res = []
    str_date, str_time = None, None
    if mode == "Start":
        str_date = df.Start_Date
        str_time = df.Start_Time
    else: 
        str_date = df.End_Date
        str_time = df.End_Time

    for i in range(len(str_date)):
        datetime_obj = convert_datetime_to_datetime_obj(str_date, str_time, i)
        if datetime_obj != None:
            datetime_res.append(datetime_obj)

    return datetime_res

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
