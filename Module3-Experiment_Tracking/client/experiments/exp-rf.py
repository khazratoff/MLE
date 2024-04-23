from hyperopt import hp
from sklearn.ensemble import RandomForestClassifier
from experiment import BaseExperiment

random_forests_experiment = BaseExperiment(
    experiment_name="RANDOM_FORESTS-DIGIT_CLASSIFICATION",
    tracking_uri="http://mlflow-server:5000",
    tag="random-forests",
    classifier=RandomForestClassifier,
    registered_model_name="rand-forest-model",
    search_space={
        "n_estimators": hp.choice("n_estimators", [50, 100, 150, 200]),
        "max_depth": hp.choice("max_depth", [None, 5, 10, 15, 20]),
        "min_samples_split": hp.choice("min_samples_split", [2, 5, 10]),
        "min_samples_leaf": hp.choice("min_samples_leaf", [1, 2, 4]),
    },
)
random_forests_experiment.run_experiment()
random_forests_experiment.save_best_model()
