import mlflow
import os
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
from experiment import BaseExperiment


# Creating XGBoost Experiment class with BaseExperiment as parent class
class XGBoostExperiment(BaseExperiment):
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
        super().__init__(
            experiment_name,
            tracking_uri,
            tag,
            classifier,
            registered_model_name,
            search_space,
            artifact_path,
        )

    def run_experiment(self):
        mlflow.set_tracking_uri(self.tracking_uri)
        mlflow.set_experiment(self.experiment_name)

        def objective(params):
            with mlflow.start_run():
                mlflow.set_tag("model", self.tag)
                mlflow.log_params(params)
                clf = XGBClassifier(**params)
                evaluation = [(self.x_train, self.y_train), (self.x_test, self.y_test)]
                clf.fit(
                    self.x_train,
                    self.y_train,
                    eval_set=evaluation,
                    early_stopping_rounds=10,
                    verbose=False,
                )
                y_pred = clf.predict(self.x_test)
                accuracy = accuracy_score(self.y_test, y_pred)
                mlflow.log_metric("accuracy", accuracy)
                f1 = f1_score(self.y_test, y_pred, average="micro")
                mlflow.log_metric("f1_score", f1)
                mlflow.xgboost.log_model(
                    xgb_model=clf,
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
        loaded_model = mlflow.xgboost.load_model(f"runs:/{self.run_id}/mlruns")
        if not os.path.exists(self.best_models_dir):
            os.makedirs(self.best_models_dir, exist_ok=True)
        best_model_path = os.path.join(self.best_models_dir, "xgboost_best_model")
        mlflow.xgboost.save_model(loaded_model, best_model_path)


xgboost_experiment = XGBoostExperiment(
    experiment_name="XGBOOST-DIGIT_CLASSIFICATION",
    tracking_uri="http://mlflow-server:5000",
    tag="xgboost",
    classifier=XGBClassifier,
    registered_model_name="xgboost-model",
    search_space={
        "learning_rate": hp.choice("learning_rate", [0.0005, 0.001, 0.01, 0.5, 1]),
        "max_depth": hp.choice("max_depth", range(3, 21, 3)),
        "gamma": hp.choice("gamma", [i / 10.0 for i in range(0, 5)]),
        "colsample_bytree": hp.choice(
            "colsample_bytree", [i / 10.0 for i in range(3, 10)]
        ),
        "reg_alpha": hp.choice("reg_alpha", [1e-5, 1e-2, 0.1, 1, 10, 100]),
        "reg_lambda": hp.choice("reg_lambda", [1e-5, 1e-2, 0.1, 1, 10, 100]),
        "seed": hp.choice("seed", [0, 7, 42]),
    },
)

xgboost_experiment.run_experiment()
xgboost_experiment.save_best_model()
