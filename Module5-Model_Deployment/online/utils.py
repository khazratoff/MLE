import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
INFERENCE_DATA_PATH = os.path.join(ROOT_DIR, "resources/inference_data")
OUTPUT_PATH = os.path.join(ROOT_DIR, "resources/output")
MODEL_REST_API_URL = "http://localhost:5000/predict"
DATA_URL = "https://drive.google.com/drive/folders/1iIzvYuOh2nNPW048fPlbMOIdkEUqTTfR?usp=sharing"
