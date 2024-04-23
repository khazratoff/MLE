from hyperopt import hp
from sklearn.linear_model import LogisticRegression
from experiment import BaseExperiment


log_reg_experiment = BaseExperiment(
    experiment_name="LOGISTIC_REGRESSION-DIGIT_CLASSIFICATION",
    tracking_uri="http://mlflow-server:5000",
    tag="logistic_regression",
    classifier=LogisticRegression,
    registered_model_name="log_reg",
    search_space={
        "penalty": hp.choice("penalty", ["l1", "l2"]),
        "C": hp.loguniform("C", -5, 5),
        "solver": hp.choice("solver", ["liblinear", "saga"]),
    },
)
log_reg_experiment.run_experiment()
log_reg_experiment.save_best_model()
