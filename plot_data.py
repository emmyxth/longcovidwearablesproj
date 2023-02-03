from matplotlib import pyplot as plt 
import numpy as np
from data import get_train
import pandas as pd

#data = tuple of numpy arrays (X_train, T_train) where X_train is (samples, features) and T_train is (samples, 1)
#RHR = bool of whether to switch to RHR mode
def plot_data(data, RHR):
    X_train, T_train = data
    
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
        x_label = X_train.dtype.names[1] #need to change to fit
        y_label = X_train.dtype.names[2] #need to change to fit
        plt.title(f"{x_label}")
        plt.xlabel("x_label")
        plt.ylabel("y_label")
        plt.scatter(X_train[1], X_train[2])
        plt.show()
        
    plt.savefig('LongCovidProject/figures') #need to change path
