FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.11-dev AS compile-image

USER root
RUN apk add --no-cache build-base postgresql-dev

RUN mkdir /app
WORKDIR /app

RUN python3 -m venv venv
ENV PATH=/app/venv/bin:$PATH

COPY vault_to_env.sh .

RUN adduser -D -h /app/ -u 1069 -s /bin/bash speiling && \
    chown -R speiling:speiling /app/ && chmod +x vault_to_env.sh

USER speiling

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY speiling_db_bq.py .

COPY vault_to_env.sh .

ENTRYPOINT ["python3", "speiling_db_bq.py", "vault_to_env.sh"]