from datetime import datetime, timedelta 
import pandas as pd
import os 
import glob 

# Helper function 1
# Iterative Binary Search Function
# It returns the first index AFTER covid test_date 
def test_date_binary_search(df_date_col, df_time_col, test_date):
    low = 0
    high = len(df_date_col) - 2  # intentionally len(df) - 2, as the last line in df occasionally is NOT date object (error prevention)
    mid = 0
 
    while low <= high:
        mid = (high + low) // 2
        cur_date = datetime.strptime(df_date_col[mid], "%Y-%m-%d")
        cur_time_str = df_time_col[mid]
        if cur_time_str[1] == ":":  # edge case
            cur_time_str = "0" + cur_time_str
        print(df_time_col[mid])
        cur_time = datetime.strptime(cur_time_str[:8], "%H:%M:%S").time()
        cur_datetime = datetime.combine(cur_date, cur_time)
        # If date is greater, ignore left half
        if cur_datetime < test_date:
            low = mid + 1
 
        # If date is smaller, ignore right half
        elif cur_datetime > test_date:
            high = mid - 1
 
        # means exact match of date
        else:
            return mid
    
    cur_date = datetime.strptime(df_date_col[mid], "%Y-%m-%d")
    cur_time_str = df_time_col[mid]
    if cur_time_str[1] == ":":  # edge case
        cur_time_str = "0" + cur_time_str
    print(df_time_col[mid])
    cur_time = datetime.strptime(cur_time_str[:8], "%H:%M:%S").time()    
    cur_datetime = datetime.combine(cur_date, cur_time)
    
    # index "mid" is before test date
    if cur_datetime < test_date and mid < len(df_date_col) - 2:  return mid + 1
    # index "mid" is after test date
    return mid

# Helper function 2: counts data count of pre and post covid testing for each df type
def count_pre_post_test(start_path: str, participant_id: str, path_type: str, mod_test_date):
    # check if the csv file exists 
    csv_file_list = glob.glob(start_path + "/" + participant_id + path_type)
    # check if the file type exists
    if len(csv_file_list) == 0:
        return (None, None)
    # open the csv file
    print(csv_file_list[0])
    df = pd.read_csv(csv_file_list[0])
    
    try:
        pre_test_count = test_date_binary_search(df.Start_Date, df.Start_Time, mod_test_date)
        post_test_count = len(df) - 2 - pre_test_count  # -2 since last line of df often includes invalid date objects, thus ignore
    except:
        print("error with date formatting")
        return (None, None)
    
    return (pre_test_count, post_test_count)

# helper function 3
def columns_to_df(Columns: list) -> pd.DataFrame:
    df = pd.DataFrame(
        {
            "id": Columns[0],
            "covid_test_date": Columns[1],
            "date_shift": Columns[2],
            "hr_count_pre_test": Columns[3],
            "hr_count_post_test": Columns[4],
            "st_count_pre_test": Columns[5],
            "st_count_post_test": Columns[6],
            "hrv_count_post_test": Columns[7],
            "hrv_count_post_test": Columns[8],
            "sl_count_post_test": Columns[9],
            "sl_count_post_test": Columns[10],
        }
    )
    return df

"""
Creates: 

Columns = [
ID, COVID Test date, Dateshift, 
num hr data pre covid, num hr data post covid,
num st data pre covid, num st data post covid, 
num hrv data pre covid, num hrv data post covid,
num sl data pre covid, num sl data post covid
]

"""
def main(df_metadata: pd.DataFrame, start_path: str):
    # cols to fill
    ID_col, test_date_col, dateshift_col, hr_pre_col, hr_post_col = [], [], [], [], []
    st_pre_col, st_post_col, hrv_pre_col, hrv_post_col, sl_pre_col, sl_post_col = [], [], [], [], [], []
    
    line_count = 0
    
    # iterate through the IDs
    for i in range(len(df_metadata)):
        # current participant ID
        participant_id = df_metadata['numeric_id'][i]
        # check if it's a valid numeric_id (old_num_id is 16 digits long, new is longer)
        if len(str(participant_id)) > 17 and participant_id[:5] == "gxezl":
            dateshift = df_metadata['date_shift'][i]
            str_true_test_date = df_metadata['covid_test_date'][i]
            true_test_date = datetime.strptime(str_true_test_date, "%Y-%m-%d %H:%M:%S")
            # modified test date to compare later
            mod_test_date = true_test_date + timedelta(days=int(df_metadata['date_shift'][i]))
            # find counts
            hr_count_before, hr_count_after = count_pre_post_test(start_path, participant_id, 
                                                                  "/hr.csv", mod_test_date)
            st_count_before, st_count_after = count_pre_post_test(start_path, participant_id, 
                                                                  "/st.csv", mod_test_date)
            hrv_count_before, hrv_count_after = count_pre_post_test(start_path, participant_id, 
                                                                    "/heartvar.csv", mod_test_date)
            sl_count_before, sl_count_after = count_pre_post_test(start_path, participant_id, 
                                                                  "/sl.csv", mod_test_date)
            
            # fill out columns
            ID_col.append(participant_id)
            test_date_col.append(str_true_test_date)
            dateshift_col.append(dateshift)
            hr_pre_col.append(hr_count_before)
            hr_post_col.append(hr_count_after)
            st_pre_col.append(st_count_before)
            st_post_col.append(st_count_after)
            hrv_pre_col.append(hrv_count_before)
            hrv_post_col.append(hrv_count_after)
            sl_pre_col.append(sl_count_before)
            sl_post_col.append(sl_count_after)
            
            line_count += 1
            print(line_count/len(df_metadata))
            
    Columns = [ID_col, test_date_col, dateshift_col, hr_pre_col, 
               hr_post_col, st_pre_col, st_post_col, hrv_pre_col, 
               hrv_post_col, sl_pre_col, sl_post_col]
    
    return Columns 


if __name__ == "__main__":
    start_path = "/labs/mpsnyder/LongCovidEkanath/COVID_Positives/COVID_Positives_Final_data"
    os.chdir(start_path)
    participant_paths = glob.glob('*')
    metadata_csv = pd.read_csv("/labs/mpsnyder/LongCovidEkanath" +  "/" + "Modified_Metadata_Jan2023_Sheet1.csv")
    Columns = main(metadata_csv, start_path)
    df_res = columns_to_df(Columns)
    df_res.to_csv("/labs/mpsnyder/LongCovidEkanath/COVID_Positives" + "/" + "pre_post_covid_data_counts.csv")
    print("Completed")
