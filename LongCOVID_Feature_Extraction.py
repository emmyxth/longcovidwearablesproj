#!/usr/bin/env python
# coding: utf-8

# In[18]:


import pandas as pd
import numpy as np
import os
from datetime import *


# In[19]:


rootdir = "/labs/mpsnyder/long-covid-study-data/final_data"
idmapping = pd.read_csv("/home/emmyst/idmapping.csv", dtype='str')
date_format = "%Y-%m-%d"


# In[20]:

#Length of datapoints
def count_len_csv(files, path):
    total_count = 0
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        total_count += len(df)
    return total_count


# In[21]:

#Length of device usage time of first file not empty
def device_length(files, path):
    diff = []
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        date = df.loc[:, 'Start_Date']
        if not date.empty:
            start_date = date[0]
            end_date = date[len(df) -1]
            formatted_start = datetime.strptime(start_date, date_format)
            formatted_end = datetime.strptime(end_date, date_format)
            return abs(formatted_start - formatted_end)

# In[22]:

#Number of gaps in data for all metrics per participant
def gaps_numb(files, path):
    count = 0
    for f in files:
        updated = path + '/' + f
        df = pd.read_csv(updated)
        date_col = df.loc[:, 'Start_Date']
        if not date_col.empty:
            prev = datetime.strptime(date_col[0], date_format)
            for i in range(1, len(df)):
                cur_date = datetime.strptime(date_col[i], date_format)
                if cur_date - prev > timedelta(days = 3):
                    count += 1
                prev = cur_date
    return count


# In[23]:

#Average values of different features (hr, st)
def mean_features(path):
    df = pd.read_csv(path)
    if not df.empty:
        return df['Value'].mean()


# In[ ]:

#Pulling all together - finding for each participant in list
dir_list = os.listdir(rootdir)
data_count = []
gaps_count = []
device_time = []
mean_hr = []
mean_st = []
for dir in dir_list:
    path = rootdir + "/" + dir
    csv_files = os.listdir(path)
    if len(csv_files) != 0:
        data_count.append(count_len_csv(csv_files, path))
        gaps_count.append(gaps_numb(csv_files, path))
        device_time.append(gaps_numb(csv_files, path))
        if "hr.csv" in csv_files:
            mean_hr.append(mean_features(path + "/" + "hr.csv"))
        if "st.csv" in csv_files:
            mean_st.append(mean_features(path + "/" + "st.csv"))
    print("done")


# In[17]:


#Saving to csv file
data = {
    'gaps_count': gaps_count,
    'device_time': device_time,
    'mean_hr': mean_hr,
    'mean_st': mean_st
}
data = pd.DataFrame(data)
data.to_csv("/labs/mpsnyder/long-covid-study-data/processed_features/plotting")

