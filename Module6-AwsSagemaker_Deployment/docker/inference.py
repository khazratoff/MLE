import os
import joblib
import numpy as np
from flask import Flask, request, jsonify

# Load the trained model
model = joblib.load(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'models/rf_model.pkl')) 

app = Flask(__name__)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'status': 'ok'})

@app.route('/invocations', methods=['POST'])
def predict():
    # Parse input data
    input_data = request.json
    features = np.array(input_data['features'])
    
    # Perform prediction
    prediction = model.predict(features)
    
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
