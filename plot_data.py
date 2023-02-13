from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
import docopt
import os
import sys

rootpath = "/labs/mpsnyder/LongCovidEkanath/COVID_Positives/COVID_Positives_Figures"
#Main function pulling together plotting
def plot_data(data, feature, RHR):
    #X_train, T_train = data
    
    if RHR:
        plt.title("Average night RHR (11pm to 6am) from 15 days before COVID test to 90 days after COVID test date")
        plt.xlabel("Days")
        plt.ylabel("RHR")
        SD_RHR_pCovid = (X_train["SD RHR pre-covid"]) * 2 # 2 x S.D of average nightly RHR for period -45 to -15 days before COVID test date -- MAY NOT NEED THIS ASK ELY
        #for each participant in the list, generate plot
        for i in range(len(X_train)):
            id = X_train[i]["id"] #participant ID
            covid_date = X_train[i]["covid date"] #date they got COVID
            RHR = X_train["RHR"] #entire RHR column
            dates = X_train["RHR dates"] #associated dates w RHR data
            col = np.where((RHR > SD_RHR_pCovid and dates > covid_date),'r', 'b') #any day with average nightly RHR above 2 S.Ds of the preCOVID period as red point and this marking to be done for the post COVID test date period only. Produces color list
            plt.scatter(RHR, dates, c=col, linewidths=2.0) #generating plot
            plt.show()
    
    else:
        bins = find_ranges(data, feature) #finding intervals for bar chart
        data["bins"] = pd.cut(data[feature], bins=bins) #binning original data in intervals
        bin_counts = data['bins'].value_counts(sort=False) #count number of values within bin
        title, xlabel, ylabel = labels(feature) #etracting features
        fig, axs = plt.subplots(figsize=(12, 4)) 
        plot = bin_counts.plot.bar(ax=axs) #plotting data 
        axs.set_xlabel(xlabel)
        axs.set_ylabel(ylabel)
        axs.set_title(title)
        file_path = os.path.join(rootpath, feature + '.png')
        print(file_path)
        #plot = bin_counts.plot.bar(title=title, xlabel=xlabel, ylabel=ylabel) #plotting data
        axs.margins(0.2, 0.2)
        #fig.savefig(fname=file_path, format='png', pad_inches=1) #X axis cut off
        plt.show()

#returns title, x, y labels based on feature 
def labels(feature):
    title, xlabel, ylabel = None, None, None
    if feature == "mean_st":
        title = "Distribution of mean step count among COVID-19 Positive participants"
        xlabel = "Mean step count"
        ylabel = "Participant frequency"
    elif feature == "data_count":
        title = "Distribution of the amount of data per COVID-19 Positive participant"
        xlabel = "Points of data"
        ylabel = "Participant frequency"
    elif feature == "num_gaps":
        title = "Distribution of the number of gaps (>3 days) of data per COVID-19 Positive participant"
        xlabel = "Number of gaps (>3 days)"
        ylabel = "Participant frequency"
    elif feature == "device_time":
        title = "Distribution of duration of data per COVID-19 Positive participant"
        xlabel = "Number of days of data"
        ylabel = "Participant frequency"
    elif feature == "mean_hr":
        title = "Distribution of mean heart rate per COVID-19 Positive participant"
        xlabel = "Mean heart rate"
        ylabel = "Participant frequency"
    elif feature == "adherence":
        title = "Distribution of adherence per COVID-19 Positive participant"
        xlabel = "Days of active data collection / Total number of recorded days"
        ylabel = "Participant frequency"
    elif feature == "RHR":
        title = "Distribution of average night RHR (11pm to 6am) from 15 days before COVID test to 90 days after COVID test date per COVID-19 Positive participant"
        xlabel = "Days"
        ylabel = "RHR"
    return (title, xlabel, ylabel)

#Returns list of 10 evenly spaced intervals from given data values
def find_ranges(data, col):
    data[col] = data[col].replace([-1], np.NaN)
    col_data = data[col]
    max_v = col_data.max()
    min_v = col_data.min()
    rounded_intervals = np.ceil((max_v - min_v) / 10)
    return [i * rounded_intervals for i in range(11)]
    
#Read path to CSV
def read_data(path):
    arr = pd.read_csv(path, index_col=None)
    return arr

#Sample use of plotting features
src_path = "/labs/mpsnyder/long-covid-study-data/processed_features/processed_features_b1 (1).csv"
data = read_data(src_path)
plot_data(data, "device_time", False)