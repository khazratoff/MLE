FROM apache/airflow:2.9.0

RUN pip install scikit-learn pandas numpy

USER root
WORKDIR /opt/airflow

COPY /data/ /opt/airflow/data/
COPY /src/ /opt/airflow/src/
COPY /dags/ /opt/airflow/dags/


EXPOSE 8080

COPY airflow_run.sh /airflow_run.sh
RUN chmod +x /airflow_run.sh

ENTRYPOINT [ "/airflow_run.sh" ]
