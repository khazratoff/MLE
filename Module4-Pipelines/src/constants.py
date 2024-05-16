import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(path)

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_PATH = os.path.join(ROOT_DIR, "data/")
SOURCE_PATH = os.path.join(DATA_PATH, "raw/human_factor_data.csv")
EXTERNAL_SOURCE_PATH = os.path.join(DATA_PATH, "raw/edu_factor_data.csv")
PROCESSED_DATA_PATH = os.path.join(DATA_PATH, "processed/")