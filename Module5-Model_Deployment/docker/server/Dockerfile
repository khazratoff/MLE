FROM python:3.11.6-slim

WORKDIR /app

RUN pip install --no-cache-dir pillow==10.0.1 flask==3.0.3 tensorflow==2.15.0 h5py==3.10.0 numpy==1.23.5

COPY /src/ICMD/utils.py /app/utils.py
COPY /src/ICMD/online /app/online

EXPOSE 5000

CMD ["python","online/app.py"]