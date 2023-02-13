#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
from datetime import *
import math
import sys
from csv import DictWriter


# In[2]:


rootdir = "/labs/mpsnyder/long-covid-study-data/final_data"
idmapping = pd.read_csv("/labs/mpsnyder/long-covid-study-data/additional_src_files/idmapping.csv", dtype='str')
date_format = "%Y-%m-%d"
ID_bottom = []


# In[3]:


def count_len_csv(files, path):
    total_count = 0
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        total_count += len(df)
    return total_count


# In[4]:


def device_length(files, path):
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        date = df.loc[:, 'Start_Date']
        if not date.empty:
            start_date = date[0]
            end_date = date[len(df) -1]
            try:
                formatted_start = datetime.strptime(start_date, date_format)
                formatted_end = datetime.strptime(end_date, date_format)
                date_diff = str(formatted_end - formatted_start)
                day = (date_diff.split())[0]
                return int(day)
            except:
                print("Cannot convert date")


# In[5]:


def gaps_numb(files, path):
    count = 0
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        date_col = df.loc[:, 'Start_Date']
        if not date_col.empty:
            prev = datetime.strptime(date_col[0], date_format)
            for i in range(1, len(df)):
                cur_value = date_col[i]
                try:
                    cur_date = datetime.strptime(date_col[i], date_format)
                    if cur_date - prev > timedelta(days = 3):
                        count += 1
                    prev = cur_date
                except:
                    print("cannot convert date")
                    ID_bottom.append((os.path.basename(path), f))
    return count


# In[17]:


def mean_features(path):
    df = pd.read_csv(path)
    if not df.empty:
        avgs = []
        dates = df['Start_Date']
        values = df['Value']
        cur_date = dates[0]
        cur_sum = 0
        count_cur_date = 0
        for i in range(1, len(df)):
            cur_day = dates[i]
            if cur_day == cur_date and type(values[i]) != str:
                cur_sum += values[i]
                count_cur_date += 1
            else:
                avgs.append(cur_sum / count_cur_date)
                cur_date = cur_day
        return np.mean(avgs)


# In[16]:


print(mean_features("/labs/mpsnyder/long-covid-study-data/final_data/gxezl11642522163448711/hr.csv"))


# In[9]:

def add_features(participant_id):
    path = rootdir + "/" + participant_id
    csv_files = os.listdir(path)
    headers = ["id", "data_count", "num_gaps", "device_time", "mean_hr", "mean_st"]
    values = {}
    if len(csv_files) != 0:
        values["id"] = participant_id
        values["data_count"] = count_len_csv(csv_files, path)
        values["num_gaps"] = gaps_numb(csv_files, path)
        values["device_time"] = device_length(csv_files, path)
        if "hr.csv" in csv_files:
            values["mean_hr"] = mean_features(path + "/" + "hr.csv")
        if "hr.csv" not in csv_files:
            values["mean_hr"] = -1.
        if "st.csv" in csv_files:
            values["mean_st"] = mean_features(path + "/" + "st.csv")
        if "st.csv" not in csv_files:
            values["mean_st"] = -1.

    # In[ ]:


    #Saving to csv file
    with open('/labs/mpsnyder/long-covid-study-data/processed_features/processed_features_b1.csv', 'a') as f_object:
        dictwriter_object = DictWriter(f_object, fieldnames=headers)
        dictwriter_object.writerow(values)
        f_object.close()


if __name__ == "__main__":
    #### EDIT HERE, DEPENDING ON HOW BASH SCRIPT USES THIS .py FILE ####
    participant_id = os.path.basename(sys.argv[1])
    print("participant_id: ", participant_id)

    ### EDIT THE ABOVE IF DIFFERNT FORMAT ### 

    add_features(participant_id)
    print("Done extracting features for participant: ", participant_id)