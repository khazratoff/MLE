FROM python:3.11.6-slim
    

RUN apt-get update && apt-get install -y libhdf5-dev && \
    apt-get install -y cron nano && \
    apt-get clean

COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip &&\
    pip install --no-cache-dir -r /app/requirements.txt
    
WORKDIR /app
    
COPY /src/ICMD/batch/pipeline.py /app/pipeline.py
COPY /src/ICMD/utils.py /app/utils.py
COPY /src/ICMD/batch/cron.txt .


RUN crontab -u root cron.txt && rm cron.txt

    
CMD ["cron", "-f"]
