from datetime import datetime, timedelta 
import pandas as pd
import os 
import glob 
import sys

def get_datetime(df: pd.DataFrame, index: int):
    str_date, str_time = str(df.Start_Date[index]), str(df.Start_Time[index])
    # if str_date is None or str_time is None: return  
    date = datetime.strptime(str_date, "%Y-%m-%d")
    time = datetime.strptime(str_time, "%H:%M:%S").time()
    date_time = datetime.combine(date, time)
    return date_time 

def initialize_phases():
    time_phase_1, time_phase_2, time_phase_3, time_phase_4 = "23:00:00", "06:00:00", "12:00:00", "17:00:00"
    time_phase_1 = datetime.strptime(time_phase_1, "%H:%M:%S").time()
    time_phase_2 = datetime.strptime(time_phase_2, "%H:%M:%S").time()
    time_phase_3 = datetime.strptime(time_phase_3, "%H:%M:%S").time()
    time_phase_4 = datetime.strptime(time_phase_4, "%H:%M:%S").time()
    return (time_phase_1, time_phase_2, time_phase_3, time_phase_4)

def determine_phase(cur_datetime, str_date, time_phases):
    date = datetime.strptime(str_date, "%Y-%m-%d")
    art_datetime_1 = datetime.combine(date, time_phases[0])  # date 11pm -> if above, then date11pm to nextdate 6am
    art_datetime_2 = datetime.combine(date, time_phases[1])  # date 6am  -> if below, then yesterday11pm to today 6am 
    art_datetime_3 = datetime.combine(date, time_phases[2])  # date 12pm -> if below, then today6am to today 12pm
    art_datetime_4 = datetime.combine(date, time_phases[3])  # date 5pm  -> if below, then today12pm to today 5pm, if above, then today 5pm to today 11pm
    
    if cur_datetime >= art_datetime_1:
        return (0, date + timedelta(days=1))
    elif cur_datetime < art_datetime_2:
        return (0, date)
    elif cur_datetime < art_datetime_3:
        return (1, date)
    elif cur_datetime < art_datetime_4:
        return (2, date)
    else:
        return (3, date)

def create_df(columns: list) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "Device": columns[0],
            "Start_Date": columns[1],
            "eleven_to_six": columns[2],
            "six_to_twelve": columns[3],
            "twelve_to_five": columns[4],
            "five_to_eleven": columns[5],
            "daily_mean": columns[6],
        }
    )
    return df

def calc_avg_per_phase(df):
    if len(df) < 5:  return 
    #  average during 11pm to 6 am, average during 6 am to 12 pm, 
    #  average during 12 pm to 5pm and average during 5 pm to 11pm
    elev_to_six, six_to_twelve, twelve_to_five, five_to_eleven, daily = [], [], [], [], []
    device_col, date_col = [],[]
    columns = [device_col, date_col, elev_to_six, six_to_twelve, twelve_to_five, five_to_eleven, daily]
    
    time_phases = initialize_phases()
    
    index = 0
    cur_datetime = get_datetime(df, 0)
    
    cur_day = None
    while (index < len(df) - 1):
        str_date = df.Start_Date[index]
        (phase, day) = determine_phase(cur_datetime, df.Start_Date[index], time_phases)
        
        cur_day = day
        cur_day_vals = [0,0,0,0]
        cur_day_entries = [0,0,0,0]
        # while we are on the same day
        while index < len(df) - 1 and (cur_day is None or day == cur_day):
            cur_day_vals[phase] += df.Value[index]
            cur_day_entries[phase] += 1
            
            # update index, day, and phase 
            index += 1
            if index >= len(df) - 1:  
                break
            cur_datetime = get_datetime(df, index)
            (phase, day) = determine_phase(cur_datetime, df.Start_Date[index], time_phases)
        
        # At this point, we are on the next or subsequent day
        # we are on the next day, but day has not been logged yet, so log it to columns
        for i in range(len(cur_day_vals)):
            if cur_day_entries[i] != 0:
                columns[2 + i].append(cur_day_vals[i]  / cur_day_entries[i])
            else:
                columns[2 + i].append(0)
        columns[0].append(df.Device[index])
        columns[1].append(cur_day.strftime("%Y-%m-%d"))
        columns[6].append(sum(cur_day_vals) / sum(cur_day_entries))
            
    df = create_df(columns)
    
    return df

def rhr_average_by_phases(participant_id: str):
    start_path = "/labs/mpsnyder/long-covid-study-data/final_data" 
    os.chdir(start_path)
    # find hr and st csv file and check if it exists
    csv_file_path = glob.glob(start_path + "/" + participant_id + "/rhr.csv") # rhr files 
    if len(csv_file_path) == 0:  return 
    # open file
    df_src = pd.read_csv(csv_file_path[0])
    df_res = calc_avg_per_phase(df_src)

    if df_res is not None:
        df_res.to_csv(start_path + "/" + participant_id + "/rhr_mean.csv")

if __name__ == "__main__":
    # if command line format is: RHR.py [participant_id], then:
    participant_id = os.path.basename(sys.argv[1])
    print("participant_id: ", participant_id)

    ### EDIT THE ABOVE IF DIFFERNT FORMAT ### 
    rhr_average_by_phases(participant_id)
    print("Done calculating mean RHR for participant: ", participant_id)

