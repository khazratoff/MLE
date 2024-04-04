import os
import sys
import joblib
import uvicorn
from fastapi import FastAPI
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
from pydantic import BaseModel


sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils import DATA_DIR, MODEL_DIR, RESULTS_DIR


train_data = pd.read_csv(DATA_DIR+'/processed/train.csv',sep=',').drop(columns=["Unnamed: 0"])
test_data = pd.read_csv(DATA_DIR+'/processed/test.csv',sep=',').drop(columns=["Unnamed: 0"])

X = train_data.select_dtypes(include=np.number)
y = train_data['variety']
model = RandomForestClassifier()
model.fit(X,y)
print('model trained and saved successfully!')
randomizer = np.random.randint(1000,9999)
if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
joblib.dump(model,MODEL_DIR+'/model_'+str(randomizer)+'.pkl')

pred = model.predict(test_data)
res = [i for i in pred]
if not os.path.exists(RESULTS_DIR):
        os.makedirs(RESULTS_DIR)
result_dir = RESULTS_DIR+'/prediction_'+str(randomizer)+'.csv'

pd.DataFrame(data = res,columns= ['Flower class:']).to_csv(result_dir,index=False)



app = FastAPI()
HOST = '127.0.0.1'
PORT = 8000

class IrisFlower(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float
    

@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API"}

@app.get("/info")
def info():
    return 'This project aims to find the class of three type of flowers by the help of given features'

@app.post("/predict/")
def predict(data: IrisFlower):
    data = data.model_dump()
    sepal_length = data['sepal_length']
    sepal_width = data['sepal_width']
    petal_length = data['petal_length']
    petal_width = data['petal_width']

    prediction = model.predict([[sepal_length,sepal_width,petal_length,petal_width]])
    return {"Predicted class is ": prediction[0]}

if __name__ == '__main__':
    uvicorn.run(app, host=HOST, port=PORT)