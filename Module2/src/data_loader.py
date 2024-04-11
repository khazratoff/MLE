import os
import sys
import pandas as pd
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import DATA_DIR


#loading data
if not os.path.exists(DATA_DIR+'/raw/'):
        os.makedirs(DATA_DIR+'/raw/', exist_ok=True)
data = pd.read_csv(DATA_DIR+'/raw/iris.csv')

TRAIN = data[:130]
TEST = data[130:].select_dtypes(include=np.number)

#save files
if not os.path.exists(DATA_DIR+'/processed/'):
        os.makedirs(DATA_DIR+'/processed/',exist_ok=True)
TRAIN.to_csv(DATA_DIR+'/processed/train.csv')
TEST.to_csv(DATA_DIR+'/processed/test.csv')
