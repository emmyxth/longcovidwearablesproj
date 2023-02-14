#!/usr/bin/env python
# coding: utf-8


#This is an additional program that aims to add adherence metrics and mean step 
# count for each COVID-19 Positive participant
# In[1]:


import pandas as pd
import numpy as np
import os
from datetime import *
import math
import sys
from csv import DictWriter


# In[2]:


rootdir = "/labs/mpsnyder/LongCovidEkanath/COVID_Positives/COVID_Positives_Final_data"
idmapping = pd.read_csv("/labs/mpsnyder/long-covid-study-data/additional_src_files/idmapping.csv", dtype='str')
date_format = "%Y-%m-%d"


# In[3]:

#Calculating duration of data: difference between start date of first data point and start date of last data point
def device_length(date_col):
    start_date = date_col[0]
    end_date = date_col[len(date_col) - 1]
    try:
        formatted_start = datetime.strptime(start_date, date_format)
        formatted_end = datetime.strptime(end_date, date_format)
        #print("start", formatted_start, "end", formatted_end)
        date_diff = str(formatted_end - formatted_start)
        #print("date diff", date_diff)
        day = (date_diff.split())[0]
        #print("day", day)
        if day != "0:00:00":
            return int(day)
        else:
            return 0
    except:
        print("Cannot convert date")


# In[4]:

#Calculates mean step count by summing up all steps and dividing by total number of days recorded
def mean_st(path):
    df = pd.read_csv(path)
    if not df.empty:
        dates = df['Start_Date']
        values = df['Value']
        if not values.empty: #checking for empty column
            counts = [] #list of steps per day
            cur_date = dates[0]
            cur_sum = 0
            count_dates = 0
            for i in range(1, len(df)):
                cur_day = dates[i]
                if cur_day == cur_date and values[i].dtype != str: #checking if current timestamp is in same day as previous timestamp
                    cur_sum += values[i] #adding step at timestamp to that of day
                else:
                    counts.append(cur_sum)
                    count_dates += 1 #incrementing the amount of days
                    cur_date = cur_day
                    cur_sum = 0
            return np.sum(counts) / count_dates #returning steps average


# In[6]:


#Calculating adherence : number of days participant has data / total duration of data
def adherence(files, path):
    percentages = []
    for f in files:
        print(f)
        updated = path + '/' + f #specific file in each participant's folder
        df = pd.read_csv(updated, low_memory=False) #read csv file
        date_col = df.loc[:, 'Start_Date'] #extracting column
        if not date_col.empty:
            total_days = device_length(date_col) #total length of time participant had data
            if total_days:
                count = 0
                prev = datetime.strptime(date_col[0], date_format)
                #print("prev", prev)
                for i in range(1, len(date_col)):
                    if date_col[i] != "":
                        try:
                            cur_date = datetime.strptime(date_col[i], date_format)
                            if cur_date != prev:
                                count += 1
                            prev = cur_date
                        except:
                            print("cannot convert date")
                percentages.append(count / total_days)
    return np.mean(percentages)


# In[7]:


#Main function adding adherence and mean_st metrics
def add_features():
    participants = os.listdir(rootdir)
    df = pd.read_csv('/labs/mpsnyder/long-covid-study-data/processed_features/processed_features_b1 (1).csv')
    for i in range(len(df)):
        p = df.loc[i, "id"]
        print(p)
        path = rootdir + '/' + str(p)
        try:
            csv_files = os.listdir(path)
            #print(adherence(csv_files, path))
            if len(csv_files) != 0:
                df.loc[i, 'adherence'] = adherence(csv_files, path)
                if "st.csv" in csv_files:
                    df.loc[i, 'mean_st'] = mean_st(path + "/" + "st.csv")
            print(df)
        except: 
            print("ID : Not valid")
    df.to_csv('/labs/mpsnyder/long-covid-study-data/processed_features/processed_features_updated.csv')


# In[ ]:


add_features()

