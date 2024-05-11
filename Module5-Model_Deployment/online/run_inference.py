import os
import sys
import requests
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import INFERENCE_DATA_PATH, OUTPUT_PATH, MODEL_REST_API_URL


def infernce():
    images = os.listdir(INFERENCE_DATA_PATH)
    labels = []
    probabilities = []
    image_names = []
    for image_name in images:
        image = open(os.path.join(INFERENCE_DATA_PATH, image_name), "rb").read()
        payload = {"image": image}

        r = requests.post(MODEL_REST_API_URL, files=payload).json()

        if r["success"]:
            for i, result in enumerate(r["predictions"]):
                print(result["label"], f"{result['probability']*100:.2f}%")
                labels.append(result["label"])
                probabilities.append(f"{result['probability']*100:.2f}%")
                image_names.append(image_name)

        else:
            print("Request failed")
    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH, exist_ok=True)
    pd.DataFrame(
        {"Image Name": image_names, "Class": labels, "Probability": probabilities}
    ).to_csv(os.path.join(OUTPUT_PATH, "restAPI_predictions.csv"), index=False)


if __name__ == "__main__":
    infernce()
