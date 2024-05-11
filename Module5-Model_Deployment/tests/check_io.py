import os
import sys
import tensorflow as tf
import io
from PIL import Image
from keras.applications.resnet50 import decode_predictions

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import load_model, prepare_image

class TestModelIO(tf.test.TestCase):
    def test_input_output(self):
        model = load_model()
        image = open("test_img.jpeg", "rb").read()
        image = Image.open(io.BytesIO(image))
        image = prepare_image(image, target=(224, 224))

        preds = model.predict(image)

        decoded_preds = decode_predictions(preds, top=3)[0]

        self.assertAllEqual(image.shape, (1, 224, 224, 3))  # Checking input shape
        self.assertIsInstance(decoded_preds, list)    # Checking output type
        self.assertEqual(len(decoded_preds), 3)       # Checking number of predictions

if __name__ == '__main__':
    tf.test.main()
