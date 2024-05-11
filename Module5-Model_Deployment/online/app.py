import os
import sys
from keras.applications import imagenet_utils
from PIL import Image
import flask
import io

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import prepare_image, load_model

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = load_model()


@app.get("/")
def message():
    return {"message": "Keras model API is up and running!"}


@app.route("/predict", methods=["POST"])
def predict():
    # initialize the data dictionary that will be returned from the
    # view
    data = {"success": False}

    # ensure an image was properly uploaded to our endpoint
    if flask.request.method == "POST":
        if flask.request.files.get("image"):
            # read the image in PIL format
            image = flask.request.files["image"].read()
            image = Image.open(io.BytesIO(image))

            # preprocess the image and prepare it for classification
            image = prepare_image(image, target=(224, 224))

            # classify the input image and then initialize the list
            # of predictions to return to the client
            preds = model.predict(image)
            results = imagenet_utils.decode_predictions(preds, top=1)
            data["predictions"] = []

            # loop over the results and add them to the list of
            # returned predictions
            for imagenetID, label, prob in results[0]:
                r = {"label": label, "probability": float(prob)}
                data["predictions"].append(r)

            # indicate that the request was a success
            data["success"] = True

    # return the data dictionary as a JSON response
    return flask.jsonify(data)


if __name__ == "__main__":
    print(
        (
            "* Loading Keras model and Flask starting server..."
            "please wait until server has fully started"
        )
    )
    app.run()
