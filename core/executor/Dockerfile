FROM python:3.9-slim

WORKDIR /app

COPY executor.py /app/
COPY requirements.txt /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "executor.py"]
