import mlflow
import os
import sys
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(current_dir))
TRACKING_URI = "http://mlflow-server:5000"
EXPERIMENT_NAME = "XGBOOST-DIGIT_CLASSIFICATION"

sys.path.append(ROOT_DIR)
from data_loader import load_data
mlflow.set_tracking_uri(TRACKING_URI) 
mlflow.set_experiment(EXPERIMENT_NAME)

x_train, x_test, y_train, y_test = load_data()

search_space=space = {
    'learning_rate': hp.choice('learning_rate', [0.0005,0.001, 0.01, 0.5, 1]),
    'max_depth' : hp.choice('max_depth', range(3,21,3)),
    'gamma' : hp.choice('gamma', [i/10.0 for i in range(0,5)]),
    'colsample_bytree' : hp.choice('colsample_bytree', [i/10.0 for i in range(3,10)]),     
    'reg_alpha' : hp.choice('reg_alpha', [1e-5, 1e-2, 0.1, 1, 10, 100]), 
    'reg_lambda' : hp.choice('reg_lambda', [1e-5, 1e-2, 0.1, 1, 10, 100]),
    'seed': hp.choice('seed', [0,7,42])
}

def objective (params):
    with mlflow.start_run():
        mlflow.set_tag("model", "xgboost")
        mlflow.log_params(params)
        clf=XGBClassifier(**params)
        evaluation = [( x_train, y_train), (x_test, y_test)]
        clf.fit(x_train, y_train,
                eval_set=evaluation, early_stopping_rounds=10, verbose=False)
        y_pred=clf.predict(x_test)
        accuracy=accuracy_score(y_test,y_pred)
        mlflow.log_metric("accuracy", accuracy)
        f1= f1_score(y_test,y_pred,  average='micro')
        mlflow.log_metric("f1_score", f1)
        mlflow.xgboost.log_model(
        xgb_model=clf,
        artifact_path="mlruns",
        registered_model_name="xgboost",)

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
loaded_model = mlflow.xgboost.load_model(f"runs:/{run_id}/mlruns")
best_model_dir = "best_models"
if not os.path.exists(best_model_dir):
    os.makedirs(best_model_dir,exist_ok=True)
best_model_path = os.path.join(best_model_dir, "xgboost_best_model")
mlflow.xgboost.save_model(loaded_model, best_model_path)




