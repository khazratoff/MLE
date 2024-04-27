import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

DATA_PATH = "../data"
SOURCE_PATH = DATA_PATH + "/raw/human_factor_data.csv"
EXTERNAL_SOURCE_PATH = DATA_PATH + "/raw/edu_factor_data.csv"
PROCESSED_DATA_PATH = DATA_PATH + "/processed/"


class StudentPerfomanceDataPrep:
    def __init__(
        self,
        scaler,
        test_size,
        random_state,
    ) -> None:
        self.scaler = scaler
        self.test_size = test_size
        self.random_state = random_state

    def merge_external_source(self, source_path1, source_path2):
        self.source = pd.read_csv(source_path1, index_col=0)
        self.ext_source = pd.read_csv(source_path2, index_col=0)
        self.data = pd.concat([self.source, self.ext_source], axis=1)
        print("Data merged with an external source successfully")
        print(self.data.columns)

    def clean_data(self):
        categorical_col = self.data.select_dtypes(include=["object"]).columns.tolist()
        numerical_col = self.data.select_dtypes(include=["number"]).columns.tolist()
        self.data[categorical_col] = self.data[categorical_col].dropna()
        self.data[numerical_col] = self.data[numerical_col].fillna(np.median)
        print("Data cleaned successfully")

    def split_data(self):
        temp = pd.get_dummies(
            self.data,
            columns=self.data.select_dtypes(include=["object"]).columns.tolist(),
        )
        X = temp.drop("G3", axis=1).values
        y = temp["G3"].values
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state
        )
        print("Data split successfully")

    def scale_data(self):
        self.X_train = pd.DataFrame(
            self.scaler.fit_transform(self.X_train),
            columns=self.scaler.get_feature_names_out(),
        )
        self.X_test = pd.DataFrame(
            self.scaler.transform(self.X_test),
            columns=self.scaler.get_feature_names_out(),
        )
        self.y_train = pd.Series(self.y_train)
        self.y_test = pd.Series(self.y_test)
        print("Data scaled successfully")

    def save_clean_data(self):
        if not os.path.exists(PROCESSED_DATA_PATH):
            os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)
        self.X_train.to_csv(PROCESSED_DATA_PATH + "X_train.csv")
        self.X_test.to_csv(PROCESSED_DATA_PATH + "X_test.csv")
        self.y_train.to_csv(PROCESSED_DATA_PATH + "y_train.csv")
        self.y_test.to_csv(PROCESSED_DATA_PATH + "y_test.csv")
        print("Data saved successfully")
