import sys
import gdown
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from utils import DATA_URL, INFERENCE_DATA_PATH


def load_data(url):
    if not os.path.exists(INFERENCE_DATA_PATH):
        os.makedirs(INFERENCE_DATA_PATH, exist_ok=True)
    gdown.download_folder(url=url, output=INFERENCE_DATA_PATH, remaining_ok=True)


def main():
    load_data(DATA_URL)


if __name__ == "__main__":
    main()
