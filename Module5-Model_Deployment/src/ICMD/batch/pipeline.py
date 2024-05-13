import os
import sys
import io
import pandas as pd
from keras.applications import imagenet_utils
from PIL import Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import INFERENCE_DATA_PATH, OUTPUT_PATH, load_model, prepare_image

IS_DOCKER = False


def infernce(model):
    model = model
    try:
        images = os.listdir(INFERENCE_DATA_PATH)
    except:
        IS_DOCKER = True
        pardir = os.path.abspath(os.path.dirname(__file__))
        INFERENCE_DATA_PATH = os.path.abspath(
            os.path.join(pardir, "resources/inference_data")
        )
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
    if IS_DOCKER:
        OUTPUT_PATH = os.path.abspath(os.path.join(pardir, "resources/output"))
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH, exist_ok=True)
        pd.DataFrame(
            {"Image Name": image_names, "Class": labels, "Probability": probabilities}
        ).to_csv(os.path.join(OUTPUT_PATH, "batch_predictions.csv"), index=False)

    else:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH, exist_ok=True)
        pd.DataFrame(
            {"Image Name": image_names, "Class": labels, "Probability": probabilities}
        ).to_csv(os.path.join(OUTPUT_PATH, "batch_predictions.csv"), index=False)


def create_Dockerfile():
    try:
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH, exist_ok=True)
    except:
        pardir = os.path.abspath(os.path.dirname(__file__))
        OUTPUT_PATH = os.path.abspath(os.path.join(pardir, "resources/output"))
        if not os.path.exists(OUTPUT_PATH):
            os.makedirs(OUTPUT_PATH, exist_ok=True)

    with open(os.path.join(OUTPUT_PATH, "Dockerfile"), "w") as f:
        f.write(
            """
FROM python:3.11.6-slim


RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libhdf5-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /online/ /app/online/
COPY utils.py /app/utils.py

EXPOSE 5000

CMD [ "python", "/app/online/app.py"]
"""
        )


if __name__ == "__main__":
    model = load_model()
    infernce(model)
    create_Dockerfile()
