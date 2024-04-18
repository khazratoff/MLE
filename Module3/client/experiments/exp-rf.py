import mlflow
import sys
import os
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(ROOT_DIR)

from data_loader import load_data
TRACKING_URI = "http://mlflow-server:5000"
EXPERIMENT_NAME = "RANDOM_FORESTS-DIGIT_CLASSIFICATION"
mlflow.set_tracking_uri(TRACKING_URI) 
mlflow.set_experiment(EXPERIMENT_NAME)

x_train, x_test, y_train, y_test = load_data()

search_space = {
    'n_estimators': hp.choice('n_estimators', [50, 100, 150, 200]), 
    'max_depth': hp.choice('max_depth', [None, 5, 10, 15, 20]),
    'min_samples_split': hp.choice('min_samples_split', [2, 5, 10]),  
    'min_samples_leaf': hp.choice('min_samples_leaf', [1, 2, 4]),  
}

def objective (params):
    with mlflow.start_run():
        mlflow.set_tag("model", "random-forests")
        mlflow.log_params(params)
        clf=RandomForestClassifier(**params)
        # evaluation = [( x_train, y_train), (x_test, y_test)]
        clf.fit(x_train, y_train)
        y_pred=clf.predict(x_test)
        accuracy=accuracy_score(y_test,y_pred)
        mlflow.log_metric("accuracy", accuracy)
        f1= f1_score(y_test,y_pred,  average='micro')
        mlflow.log_metric("f1_score", f1)
        mlflow.sklearn.log_model(
        sk_model = clf,
        artifact_path="mlruns",
        registered_model_name="rand-forest-model",)

    return {'loss': -accuracy, 'status': STATUS_OK }

best_result = fmin(
    fn=objective,
    space=search_space,
    algo=tpe.suggest,
    max_evals=3,
    trials=Trials()
)

experiment_id = mlflow.get_experiment_by_name(EXPERIMENT_NAME).experiment_id


# Get the experiment ID
client = MlflowClient(tracking_uri=TRACKING_URI)
run = client.search_runs(
  experiment_ids=[experiment_id],
  run_view_type=ViewType.ACTIVE_ONLY,
  order_by=["metrics.accuracy DESC"]
)[0]

run_id = run.info.run_id
loaded_model = mlflow.sklearn.load_model(f"runs:/{run_id}/mlruns")
best_model_dir = "best_models"
if not os.path.exists(best_model_dir):
    os.makedirs(best_model_dir,exist_ok=True)
best_model_path = os.path.join(best_model_dir, "random-forest_best_model")
mlflow.sklearn.save_model(loaded_model, best_model_path)




