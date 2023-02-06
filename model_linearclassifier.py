"""
Sklearn linear classifier using logistic regression for mean HR and mean count, apple watch vs fitbit
Takes in 3D array with features of interest already isolated, and target array
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

class LinearClassifier():
    #say everything is positive/negative
    def __init__(self):
        """
        @param data : numpy array (samples, features)
        """
        self.lr_model = LogisticRegression()

    #returns numpy array of predictions based on majority class classifier (samples, 1)
    def fitdata(self, data, target):
        self.lr_model.fit(data, target)
    
    #returns array (samples, 1) predictions
    def predict(self, data):
        return self.lr_model.predict(data)