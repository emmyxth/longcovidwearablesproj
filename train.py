## Generates models to be applied to Long COVID data, stores in
## LongCovidProject/models/model/fold

import numpy as np
import pickle5 as pickle #for storing model
from docopt import docopt
from model_linearclassifier import LinearClassifier
from model_majorityclass import MajorityClass
import os

METADATA_PATH = "LongCovidProject/models/model/fold" #may need to adjust

#performs pickle protocol to save modle as python object
def pickle(modelName, model):
    path = METADATA_PATH + "-%d" + modelName + ".pkl"
    if not os.path.exists(path):
        with open(path, 'w') as f:
            pickle.dump({ 
                "Model": model
            }, f, pickle.HIGHEST_PROTOCOL)

def main():
    LinearClassifierModel = LinearClassifier()
    MajorityClassModel = MajorityClass()
    pickle("linear_classifier", LinearClassifierModel)
    pickle("majority_class", MajorityClassModel)

if __name__ == '__main__':
    main()