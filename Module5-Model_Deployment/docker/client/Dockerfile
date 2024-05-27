FROM python:3.11.6-slim

WORKDIR /app

COPY . /app/

RUN python -m pip install --upgrade pip && \
    python -m venv icmd_env && \
    . icmd_env/bin/activate && \
    pip install -e .

ENV PATH="/app:${PATH}"

CMD icmd_env/bin/python src/ICMD/data_loader.py && icmd_env/bin/python src/ICMD/online/run_inference.py