import os
import sys
import io
import numpy as np
import pandas as pd
from keras.applications import ResNet50
from keras.preprocessing.image import img_to_array
from keras.applications import imagenet_utils
from PIL import Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import INFERENCE_DATA_PATH, OUTPUT_PATH


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


def infernce(model):
    model = model
    images = os.listdir(INFERENCE_DATA_PATH)
    labels = []
    probabilities = []
    image_names = []
    for image_name in images:
        image = open(os.path.join(INFERENCE_DATA_PATH, image_name), "rb").read()
        image = Image.open(io.BytesIO(image))
        image = prepare_image(image, target=(224, 224))
        preds = model.predict(image)
        results = imagenet_utils.decode_predictions(preds, top=1)
        image_names.append(results[0][0][0])
        labels.append(results[0][0][1])
        probabilities.append(results[0][0][2])
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH, exist_ok=True)
    pd.DataFrame(
        {"Image Name": image_names, "Class": labels, "Probability": probabilities}
    ).to_csv(os.path.join(OUTPUT_PATH, "batch_predictions.csv"), index=False)


if __name__ == "__main__":
    model = load_model()
    infernce(model)
