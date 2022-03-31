import dataverk as dv
from google.cloud import bigquery
from dataverk_vault import api as vault_api
from google.oauth2 import service_account
import psycopg2 as pg
import pandas.io.sql as psql
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("tabellreplisering.py")

# Vault 
secrets = vault_api.read_secrets()

# Konfigurasjon av bigQuery-klient
bigQueryKlientNøkkel = secrets.pop("GCP_json")
bigQueryCredentials = service_account.Credentials.from_service_account_info(eval(bigQueryKlientNøkkel))
bigQueryKlient = bigquery.Client(credentials=bigQueryCredentials)

# Konfigurer lesing fra database
rekrutteringsbistand_creds = secrets["rekrutteringsbistand-kandidat-db-url"]
adeo, ip, creds_loc = rekrutteringsbistand_creds.split(":")
user, password = vault_api.get_database_creds(creds_loc).split(":")
connection = pg.connect(f"host={adeo} dbname=rekrutteringsbistand-kandidat user={user} password={password}")

tabeller = {
    "utfallsendring": [],
    "veilkandidat": [],
    "veilkandliste": []
}

for tabell, tabellKonfigurasjon in tabeller.items():
    sql = "select * from " + tabell
    dataframe = psql.read_sql(sql, connection)
    jobConfig = bigquery.LoadJobConfig(schema=tabellKonfigurasjon, write_disposition="WRITE_TRUNCATE")
    job = bigQueryKlient.load_table_from_dataframe(dataframe, "toi-prod-324e.kandidat_api." + tabell, job_config=jobConfig)
    job.result()
    logger.info("Har speilet tabell " + tabell + " til BigQuery")

logger.info("Ferdig med speiling av alle tabeller")
exit(0)
