"""
As per GitHub description: "Takes a model, flags (e.g. valid or test) 
and predicts on the valid or test set". More specifically, is called by 
predict.sh with various flags to make predictions.
"""
import math
import sys
import pickle
import time
import pandas as pd


from docopt import docopt
import numpy as np
from tqdm import tqdm
from typing import List, Tuple, Dict, Set, Union
from model_linearclassifier import LinearClassifier
from model_majorityclass import MajorityClass

#Uisng linear classification (regression) to make predictions. Imports
#the model from local file - may need to unpickle packages in later iterations
def linear(args: Dict):
    src = pd.read_csv(args['--src'])
    tgt = pd.read_csv(args['--tgt'])

    model = LinearClassifier()
    model.fitdata(src, tgt) #training model
    predictions = model.predict(src)
    print("Linear Model predictions: ", predictions)
    return predictions

#Function performing majority classification by importing local
#model - may need to unpickle packages later
def majorityClass(args: Dict):
    src = pd.read_csv(args['--src'])
    tgt = pd.read_csv(args['--tgt'])

    model = MajorityClass()
    predictions = model.fitdata(tgt)
    print("Majority Model predictions: ", predictions)
    return predictions

def main():
    """ Main func. Arguments can include
    @ --maj : majority classification
    @ --lin : linear classification
    @ --src= : path to csv containing src data to be read into Pandas dataframe
    @ --tgt= : path to csv containing target data with labels to be read into Pandas dataframe
    """
    args = docopt(__doc__)

    if args['maj']:
        majorityClass(args)
    elif args['lin']:
        linear(args)
    else:
        raise RuntimeError('invalid run mode')


if __name__ == '__main__':
    main()