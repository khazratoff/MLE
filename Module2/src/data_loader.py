import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import DATA_DIR

#loading data
data = pd.read_csv(DATA_DIR+'/raw/iris.csv')

TRAIN = data[:130]
TEST = data[130:].select_dtypes(include=np.number)

#save files
TRAIN.to_csv(DATA_DIR+'/processed/train.csv')
TEST.to_csv(DATA_DIR+'/processed/test.csv')
