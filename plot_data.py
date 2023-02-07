from matplotlib import pyplot as plt 
import numpy as np
import pandas as pd
import docopt
import os
import sys

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
        col = data.loc[:, feature]
        col = count_frequencies(col.sort_values(), feature)
        plt.title(f"{feature}")
        plt.xlabel(feature)
        plt.ylabel("Participant frequency")
        x = col.loc[:,feature]
        y = col.loc[:,"counts"]
        print(x,y)
        plt.scatter(x, y)
        plt.show()
        #plt.savefig('/labs/mpsnyder/long-covid-study-data/figures/' + feature + '.png')

def count_frequencies(data, feature):
    print(data.value_counts())
    data = data.value_counts().rename_axis(feature).reset_index(name='counts')
    print(data)
    return data
    
def read_data(path):
    arr = pd.read_csv(path, index_col=None)
    print(arr)
    return arr

def main():
    feature, src_path = sys.argv[1], sys.argv[2]
    data = read_data(src_path)
    if feature == "rhr":
        plot_data(data, feature, True)
    else:
        plot_data(data, feature, False)

if __name__ == '__main__':
    main()