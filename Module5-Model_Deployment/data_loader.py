import gdown
import os
from utils import DATA_URL


def load_data(url):
    data_dir = os.path.join(os.path.dirname(__file__), "resources/inference_data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    gdown.download_folder(url=url, output=data_dir, remaining_ok=True)


if __name__ == "__main__":
    load_data(DATA_URL)
