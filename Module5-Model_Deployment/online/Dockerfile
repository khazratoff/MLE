FROM python:3.11.6-slim


RUN pip install --upgrade pip
RUN apt-get update && apt-get install -y libhdf5-dev

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

COPY /online/ /app/online/
COPY data_loader.py /app/data_loader.py

EXPOSE 5000

CMD [ "python", "/app/online/app.py"]
