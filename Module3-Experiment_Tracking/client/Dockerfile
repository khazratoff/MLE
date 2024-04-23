FROM python:3.11.6-slim

WORKDIR /mlflow_app

RUN pip install --no-cache-dir mlflow hyperopt scikit-learn numpy pandas xgboost

COPY /client/ /mlflow_app/client/
COPY data_loader.py /mlflow_app/data_loader.py

RUN chmod +x /mlflow_app/client/experiments/run.sh

ENTRYPOINT [ "/mlflow_app/client/experiments/run.sh" ]
