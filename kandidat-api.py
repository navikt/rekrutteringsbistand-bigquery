import dataverk as dv
from google.cloud import bigquery
from dataverk_vault import api as vault_api
from google.oauth2 import service_account
import psycopg2 as pg
import pandas.io.sql as psql
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("kandidat-api.py")

try:
    secrets = vault_api.read_secrets()
except:
    logger.error("Kunne ikke hente secrets fra Vault")
    exit(1)

try:
    bigQueryKlientNøkkel = secrets.pop("GCP_json")
    bigQueryCredentials = service_account.Credentials.from_service_account_info(eval(bigQueryKlientNøkkel))
    bigQueryKlient = bigquery.Client(credentials=bigQueryCredentials)
except:
    logger.error("Kunne ikke lage BigQuery-klient")
    exit(1)

try:
    kandidat_api_creds = secrets["rekrutteringsbistand-kandidat-db-url"]
    adeo, ip, creds_loc = kandidat_api_creds.split(":")
    user, password = vault_api.get_database_creds(creds_loc).split(":")
    connection = pg.connect(f"host={adeo} dbname=rekrutteringsbistand-kandidat user={user} password={password}")
except:
    logger.error("Kunne ikke opprette databaseklient")
    exit(1)

# Dictionary med tabellnavn og liste for konfigurasjon av hvordan kolonner skal tolkes
# Eksempel på kolonnekonfigurasjon: bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING)
tabeller = {
    "utfallsendring": [],
    "veilkandidat": [],
    "veilkandliste": [],
    "veilkandidatnotat": [],
    "avviksrapportering": [],
    "formidlingavusynligkandidat": [],
    "sending_av_kandidathendelse": [],
}

for tabell, tabellKonfigurasjon in tabeller.items():
    try:
        sql = "select * from " + tabell
        dataframe = psql.read_sql(sql, connection)
        dataframe.columns = dataframe.columns.str.replace("å", "aa")
        jobConfig = bigquery.LoadJobConfig(schema=tabellKonfigurasjon, write_disposition="WRITE_TRUNCATE")
        job = bigQueryKlient.load_table_from_dataframe(dataframe, "toi-prod-324e.kandidat_api." + tabell, job_config=jobConfig)
        job.result()
        logger.info("Har speilet tabell " + tabell + " til BigQuery")
    except:
        logger.error("Kunne ikke speile tabell " + tabell + " til BigQuery")
        exit(1)

logger.info("Ferdig med speiling av alle tabeller")
exit(0)
