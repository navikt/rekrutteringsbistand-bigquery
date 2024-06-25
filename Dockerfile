FROM python:3.9-slim

RUN apt-get update -y && apt-get install -y build-essential libpq-dev

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY speiling_db_bq.py .

CMD ["python3", "speiling_db_bq.py"]