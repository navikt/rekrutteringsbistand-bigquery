FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.11

#RUN apk add --no-cache build-essential libpq-dev

RUN apk add --no-cache gcc musl-dev postgresql-dev

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY speiling_db_bq.py .

COPY vault_to_env.sh .

CMD ["python3", "speiling_db_bq.py", "vault_to_env.sh"]