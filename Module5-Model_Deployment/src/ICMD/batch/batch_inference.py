import os
import sys
import io
import pandas as pd
from keras.applications import imagenet_utils
from PIL import Image


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import INFERENCE_DATA_PATH, OUTPUT_PATH, load_model, prepare_image


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


def create_Dockerfile():

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH, exist_ok=True)

    with open(os.path.join(OUTPUT_PATH, "Dockerfile"), "w") as f:
        f.write(
            """
FROM python:3.11.6-slim

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip && \
    python -m venv icmd_env && \
    . icmd_env/bin/activate && \
    pip install -e .

ENV PATH="/app:${PATH}"

CMD icmd_env/bin/python src/ICMD/data_loader.py && icmd_env/bin/python src/ICMD/online/run_inference.py
"""
        )


def main():
    model = load_model()
    infernce(model)
    create_Dockerfile()


if __name__ == "__main__":
    main()
