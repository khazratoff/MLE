FROM python:3.11.6-slim
WORKDIR /opt/program

# ENV PYTHONUNBUFFERED=TRUE
# ENV PYTHONDONTWRITEBYTECODE=TRUE
# ENV PATH="/opt/program"
COPY docker /opt/program
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8080

ENV NAME RandomForestIris

RUN chmod +x /opt/program/inference.py

ENTRYPOINT ["python", "/opt/program/inference.py"]
