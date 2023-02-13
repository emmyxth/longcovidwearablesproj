import os
import pandas as pd
import numpy as np
import sys

COVID_STUDY_PATH = "/labs/mpsnyder/long-covid-study-data/COVID_GCB/covid-study/"
LONG_COVID_STUDY_PATH = "/labs/mpsnyder/long-covid-study-data/longcovid2022-study/longcovid2022-processed/"
SCG_FOLDER_PATH = "/labs/mpsnyder/long-covid-study-data/LongCOVIDSCG/"
OUTPUT_FOLDER_PATH = "/labs/mpsnyder/long-covid-study-data/final_data_cleaned/"
COLUMN_NAMES = ['Device','Start_Date','End_Date','Start_Time','End_Time','Value','Tag','Type']

def get_id_mapping():
    '''
    This function reads in the id mapping file and returns it as a pandas dataframe

    Returns:
        id_mapping (pandas dataframe): the id mapping file
    '''
    id_mapping = pd.read_csv("/labs/mpsnyder/long-covid-study-data/additional_src_files/idmapping.csv", dtype = "str")
    return id_mapping

def get_covid_study_data(id: str, data_type: str) -> pd.DataFrame:
    '''
    This function reads in the data from the covid study and returns it as a pandas dataframe

    Args:
        id (str): the id of the participant
        data_type (str): the type of data to read in
    
    Returns:
        data (pandas dataframe): the data from the covid study (empty dataframe if the data doesn't exist)
    '''

    # map the different types of data to the different paths
    data_formats = {
        "hr": "/hr/hr.csv",
        "st": "/st/st.csv",
        "sl": "/sl/sl.csv"
    }
    
    file_name = data_formats[data_type]

    # set up the paths to the data
    file_path = os.path.join(COVID_STUDY_PATH, id, file_name)
    
    return get_csv_data(file_path)

def get_long_covid_study_data(id: str, data_type: str) -> pd.DataFrame:
    '''
    This function reads in the data from the long covid study and returns it as a pandas dataframe

    Args:
        id (str): the id of the participant
        data_type (str): the type of data to read in
    
    Returns:
        data (pandas dataframe): the data from the covid study (empty dataframe if the data doesn't exist)
    '''
    # map the different types of data to the different paths
    data_formats = {
        "hr": "/hr.csv",
        "st": "/st.csv",
        "sl": "/sl.csv"
    }

    file_name = data_formats[data_type]

    # set up the paths to the data
    file_path = os.path.join(LONG_COVID_STUDY_PATH, id, file_name)

    return get_csv_data(file_path)

def get_csv_data(file_path: str) -> pd.DataFrame:
    # if the folder doesn't exist, return an empty dataframe
    if not os.path.isfile(file_path):
        return pd.DataFrame()

    # if the file is empty, return an empty dataframe
    if os.stat(file_path).st_size == 0:
        return pd.DataFrame()
    
    # try to read in the data
    # try:
    df_result = pd.read_csv(file_path, dtype = "string")
    # except Exception as e:
    #     print(e)
    #     # return an empty dataframe if there is an error
    #     return pd.DataFrame()
    
    return clean_df(df_result)

def clean_df(df_result: pd.DataFrame) -> pd.DataFrame:
    '''
    This function cleans the data from the csv files and returns it as a pandas dataframe
    1. make sure all columns are present
    2. drop all the rows that value is not a integer
    3. rearrage the columns so that it is the same order as COLUMN_NAMES

    Args:
        df_result (pandas dataframe): the data from the csv file

    Returns:
        df_cleaned (pandas dataframe): the cleaned data

    '''
    df_cleaned = pd.DataFrame()
    # make sure all columns are present
    for col in COLUMN_NAMES:
        # if the column is not present, add it as a column of NaNs
        if col not in df_result.columns:
            df_cleaned[col] = np.NaN
        else:
            df_cleaned[col] = df_result[col]
    
    # drop all the rows that value is not a integer
    df_cleaned = df_cleaned[df_cleaned["Value"].str.isnumeric()]
    df_cleaned["Value"] = df_cleaned["Value"].astype(int)

    # rearrage the columns so that it is the same order as COLUMN_NAMES
    df_cleaned = df_cleaned[COLUMN_NAMES]

    # convert the start time to datetime if 12 hour format
    if df_cleaned.iloc[0]['Start_Time'].endswith("M"):
        df_cleaned["Start_Time"] = pd.to_datetime(df_cleaned["Start_Time"])

    assert(df_cleaned.columns.tolist() == COLUMN_NAMES) # make sure all the columns are present

    return df_cleaned

def get_scg_data(id: str, data_type: str) -> pd.DataFrame:
    '''
    This function reads in the data from the scg study and returns it as a pandas dataframe

    Args:
        id (str): the id of the participant
        data_type (str): the type of data to read in
    
    Returns:
        data (pandas dataframe): the data from the covid study (empty dataframe if the data doesn't exist)
    '''
    # map the different types of data to the different paths
    data_formats = {
        "hr": ["/Orig_Fitbit_HR.csv", "/Orig_NonFitbit_HR.csv"],
        "st": ["/Orig_Fitbit_ST.csv", "/Orig_NonFitbit_ST.csv"],
    }

    # if the data type is sl, return an empty dataframe
    if data_type == "sl":
        return pd.DataFrame()

    # set up the paths to the data
    file_paths = [os.path.join(SCG_FOLDER_PATH, "All_others_wearable_data_Mar2022", id, file_name) for file_name in data_formats[data_type]]
    file_paths += [os.path.join(SCG_FOLDER_PATH, "All_positives_wearable_data_Mar2022", id, file_name) for file_name in data_formats[data_type]]
    file_paths += [os.path.join(SCG_FOLDER_PATH, "Older", id, file_name) for file_name in data_formats[data_type]]

    # remove any paths that don't exist
    file_paths = [file_path for file_path in file_paths if os.path.isfile(file_path)]

    # if there are no file paths, return an empty dataframe
    if len(file_paths) == 0:
        return pd.DataFrame()
    
    assert(len(file_paths) == 1) # make sure there is only one file path

    file_path = file_paths[0]

    # if the file is empty, return an empty dataframe
    if os.stat(file_path).st_size == 0:
        return pd.DataFrame()

    # try to read in the data
    df_result = pd.read_csv(file_paths[0], dtype = "string")

    # add device column
    if os.path.basename(file_path) == "/Orig_Fitbit_HR.csv" or os.path.basename(file_path) == "/Orig_Fitbit_ST.csv":
        df_result["device"] = "Fitbit"
    
    df_result[['Start_Date','Start_Time']] = df_result["datetime"].str.split(n=1, expand=True)
    df_result = df_result.rename(columns={"device": "Device", "heartrate": "Value", "steps": "Value"})
    
    return clean_df(df_result)

def data_joining(id: str):
    '''
    This function joins the data from the different studies and saves it as a csv file

    Args:
        index (int): the index of the participant in the id mapping file

    Returns:
        None
    '''

    # # read in the id mapping file
    # id_mapping = get_id_mapping()
    # id = id_mapping["Long COVID BUcket ID"].iloc[index]
    data_formats = ["hr", "st", "sl"]

    # check if the output folder exists
    if not os.path.isdir(OUTPUT_FOLDER_PATH):
        os.mkdir(OUTPUT_FOLDER_PATH)

    for data_format in data_formats:
        # get the data from the csv files
        scg_data = get_scg_data(id, data_format)
        covid_study_data = get_covid_study_data(id, data_format)
        long_covid_study_data = get_long_covid_study_data(id, data_format)

        # join the data
        data = pd.concat([scg_data, covid_study_data, long_covid_study_data], ignore_index = True)

        if data.empty:
            continue
        
        # sort the data by date
        data = data.sort_values(by=["Start_Date", "Start_Time"], ascending=[True, True], ignore_index = True, na_position = "first")

        output_folder_path = os.path.join(OUTPUT_FOLDER_PATH, id)

        # check if the output folder exists
        if not os.path.isdir(output_folder_path):
            os.mkdir(output_folder_path)
        
        assert(data.columns.tolist() == COLUMN_NAMES) # make sure all the columns are present

        # save the data as a csv file
        data.to_csv(os.path.join(output_folder_path, data_format + ".csv"), index = False)
    
if __name__ == "__main__":
    # command line argument is the index of the participant in the id mapping file
    index = os.path.basename(sys.argv[1])
    participant_id = get_id_mapping()["Long COVID BUcket ID"].iloc[int(index)]
    print("participant_id: ", participant_id)

    data_joining(participant_id)

    print("Done extracting RHR for participant: ", participant_id)
