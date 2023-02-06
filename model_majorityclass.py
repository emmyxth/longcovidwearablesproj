"""
Majority class classifier model: takes in array of dimension (samples, 1) of T_train
and returns array of dimension (samples, 1) of predictions
"""

import numpy as np
import pandas as pd

class MajorityClass():
    #say everything is positive/negative
    def __init__(self):
        self.nsamples = 0

    #returns numpy array of predictions based on majority class classifier (samples, 1)
    def fitdata(self, data):
        self.nsamples = len(data)
        count_neg, count_pos = 0, 0
        for i in range(self.nsamples):
            if data[i] == "neg":
                count_neg += 1
            else:
                count_pos += 1
        if count_neg > count_pos:
            return ["neg" for i in range(self.nsamples)]
        else:
            return ["pos" for i in range(self.nsamples)]
    