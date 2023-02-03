from datetime import datetime, timedelta 

"""
Description: The function converts str date, "%Y-%m-%d", and str time, "%H:%M:%S", to datetime object: "%Y-%m-%d %H:%M:%S"

params: df -> dataframe of EITHER hr.csv or st.csv 
index: index of df's column: e.g. index = 5 if we want to access the str date df.Start_date[index]

returns: converted & combined datetime of the form "%Y-%m-%d %H:%M:%S"
"""
def convert_datetime_to_datetime_obj(df, index):
    str_date, str_time = df.Start_Date[index], df.Start_Time[index]
    date = datetime.strptime(str_date, "%Y-%m-%d")
    time = datetime.strptime(str_time, "%H:%M:%S").time()
    date_time = datetime.combine(date, time)
    return date_time 


