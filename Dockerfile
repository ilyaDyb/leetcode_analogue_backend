FROM python:3.10

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && \
    apt-get install -y apt-transport-https ca-certificates curl gnupg2 software-properties-common && \
    curl -fsSL https://get.docker.com -o get-docker.sh && \
    sh get-docker.sh --install-branch=stable --skip-add-user

COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
