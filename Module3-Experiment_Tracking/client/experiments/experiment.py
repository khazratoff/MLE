import mlflow
import sys
import os
from hyperopt import STATUS_OK, Trials, fmin, tpe
from sklearn.metrics import accuracy_score, f1_score
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType

current_dir = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(current_dir))
sys.path.append(ROOT_DIR)
from data_loader import load_data


class BaseExperiment:
    def __init__(
        self,
        experiment_name,
        tracking_uri,
        tag,
        classifier,
        registered_model_name,
        search_space,
        artifact_path="mlruns",
    ) -> None:
        self.experiment_name = experiment_name
        self.tracking_uri = tracking_uri
        self.tag = tag
        self.search_space = search_space
        self.classifier = classifier
        self.artifact_path = artifact_path
        self.registered_model_name = registered_model_name
        self.x_train, self.x_test, self.y_train, self.y_test = load_data()
        self.run_id = None
        self.best_models_dir = "best_models"

    def run_experiment(self):
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

        def objective(params):
            with mlflow.start_run():
                mlflow.set_tag("model", self.tag)
                mlflow.log_params(params)
                clf = self.classifier(**params)
                clf.fit(self.x_train, self.y_train)
                y_pred = clf.predict(self.x_test)
                accuracy = accuracy_score(self.y_test, y_pred)
                mlflow.log_metric("accuracy", accuracy)
                f1 = f1_score(self.y_test, y_pred, average="micro")
                mlflow.log_metric("f1_score", f1)
                mlflow.sklearn.log_model(
                    sk_model=clf,
                    artifact_path=self.artifact_path,
                    registered_model_name=self.registered_model_name,
                )

            return {"loss": -accuracy, "status": STATUS_OK}

        best_result = fmin(
            fn=objective,
            space=self.search_space,
            algo=tpe.suggest,
            max_evals=3,
            trials=Trials(),
        )
        experiment_id = mlflow.get_experiment_by_name(
            self.experiment_name
        ).experiment_id
        client = MlflowClient(tracking_uri=self.tracking_uri)
        run = client.search_runs(
            experiment_ids=[experiment_id],
            run_view_type=ViewType.ACTIVE_ONLY,
            order_by=["metrics.accuracy DESC"],
        )[0]
        self.run_id = run.info.run_id
        return best_result

    def save_best_model(self):
        loaded_model = mlflow.sklearn.load_model(f"runs:/{self.run_id}/mlruns")
        if not os.path.exists(self.best_models_dir):
            os.makedirs(self.best_models_dir, exist_ok=True)
        best_model_path = os.path.join(
            self.best_models_dir, self.registered_model_name + "_best_model"
        )
        mlflow.sklearn.save_model(loaded_model, best_model_path)
