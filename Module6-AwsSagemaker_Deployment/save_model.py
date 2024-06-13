import joblib
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris


def train_model():
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier()
    model.fit(X, y)
    print("model trained successfully!")
    return model


def save_model(model):
    model = model
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docker/models")
    if not os.path.exists(model_path):
        os.makedirs(model_path, exist_ok=True)
    joblib.dump(model, os.path.join(model_path, "rf_model.pkl"))

    # with tarfile.open('model.tar.gz', 'w:gz') as tar:
    #     tar.add(os.path.join(model_path, "rf_model.pkl"), arcname='rf_model.pkl')

    # s3 = boto3.client('s3')
    # bucket_name = 'awsbucketforml'
    # s3_path = 'mlmodel/model.tar.gz' 
    # s3.upload_file('model.tar.gz', bucket_name, s3_path)

    # print(f'Model uploaded to s3://{bucket_name}/{s3_path}')


if __name__ == "__main__":
    model = train_model()
    save_model(model)



