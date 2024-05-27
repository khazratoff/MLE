import os
import numpy as np
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils


ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "..")
)
INFERENCE_DATA_PATH = os.path.join(ROOT_DIR, "resources/inference_data")
OUTPUT_PATH = os.path.join(ROOT_DIR, "resources/output")
HOST = os.getenv("FLASK_SERVER_HOST", "localhost")
MODEL_REST_API_URL = f"http://{HOST}:5000/predict"
DATA_URL = "https://drive.google.com/drive/folders/1bnNR9WhnY-cEjqkBvpRoh2antY4kEttG?usp=sharing"


def load_model():
    print("[INFO] loading model...")
    model = ResNet50(weights="imagenet")
    return model


def prepare_image(image, target):
    if image.mode != "RGB":
        image = image.convert("RGB")

    image = image.resize(target)
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = imagenet_utils.preprocess_input(image)
    return image
