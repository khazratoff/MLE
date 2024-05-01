# Use the official Airflow image from Docker Hub
FROM apache/airflow:2.9.0

# Install supervisord
RUN pip install scikit-learn pandas numpy

USER root
# Create directories for data, scripts, and DAGs
WORKDIR /opt/airflow


# Copy data, scripts, and DAGs into the container
COPY /data/ /opt/airflow/data/
COPY /src/ /opt/airflow/src/
COPY /dags/ /opt/airflow/dags/


# Expose the Airflow webserver port
EXPOSE 8080

COPY airflow_run.sh /airflow_run.sh
RUN chmod +x /airflow_run.sh

# Start supervisord
ENTRYPOINT [ "/airflow_run.sh" ]
