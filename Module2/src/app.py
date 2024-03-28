import uvicorn
from fastapi import FastAPI
from IrisFlower import IrisFlower
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import pandas as pd
print("Starting...\U0001f600")

iris = load_iris()
X, y = iris.data, iris.target
print("Loading Iris dataset...")
model = RandomForestClassifier()
model.fit(X, y)

print("Training using RandomForestClassifier model...")
app = FastAPI(title="Iris Flower Classification API",)



@app.get("/")
def read_root():
    return {"message": "Welcome to the ML Model API"}

@app.get("/info")
def info():
    return 'This project aims to find the class of three type of flowers by the help of given features'

@app.post("/predict/")
def predict(data: IrisFlower):
    df = pd.DataFrame([data.model_dump()])
    prediction = model.predict(df)
    class_name = iris.target_names[prediction][0]
    return {"Predicted class is ": class_name}


if __name__ == '__main__':
    
    uvicorn.run(app, host='127.0.0.1', port=8000)