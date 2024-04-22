from sklearn import datasets
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

def load_data():
    digits = datasets.load_digits() 
    x = digits.data               
    y = digits.target 
    df = pd.DataFrame(data= np.c_[digits['data'], digits['target']],
                        columns= digits['feature_names'] + ['target'])
    x_train, x_test, y_train, y_test = train_test_split(df[digits['feature_names']], df['target'], test_size=0.2, random_state=42)

    return x_train,x_test,y_train,y_test