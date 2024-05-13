import gdown
import os
from utils import DATA_URL, INFERENCE_DATA_PATH


def load_data(url):
    if not os.path.exists(INFERENCE_DATA_PATH):
        os.makedirs(INFERENCE_DATA_PATH, exist_ok=True)
    gdown.download_folder(url=url, output=INFERENCE_DATA_PATH, remaining_ok=True)


if __name__ == "__main__":
    load_data(DATA_URL)
