import os
from google.cloud import bigquery
from google.oauth2 import service_account
import psycopg2 as pg
import pandas.io.sql as psql
import logging

logging.basicConfig(encoding="utf-8", level=logging.DEBUG)
logger = logging.getLogger("speiling_db_bq.py")


try:
    bigQueryKlientNøkkel = os.environ["GCP_JSON"]
    bigQueryCredentials = service_account.Credentials.from_service_account_info(
        eval(bigQueryKlientNøkkel)
    )
    bigQueryKlient = bigquery.Client(credentials=bigQueryCredentials)
except:
    logger.error("Kunne ikke lage BigQuery-klient")
    exit(1)


# Funksjon brukt for å speile tabeller fra en database til BigQuery
def speiling_db_bq(db_navn, tabeller, bigQueryKlient, logger):
    try:
        creds = os.environ[db_navn + "-db-url"]
        adeo, _, creds_loc = creds.split(":")
        user, password = os.environ[creds_loc].split(":")
        connection = pg.connect(
            f"host={adeo} dbname={db_navn} user={user} password={password}"
        )
    except:
        logger.error(f"Kunne ikke opprette databaseklient for {db_navn}")
        exit(1)

    for tabell, tabellKonfigurasjon in tabeller.items():
        try:
            sql = "select * from " + tabell
            dataframe = psql.read_sql(sql, connection)
            dataframe.columns = (
                dataframe.columns.str.replace("å", "aa")
                .str.replace("æ", "ae")
                .str.replace("ø", "o")
            )
            jobConfig = bigquery.LoadJobConfig(
                schema=tabellKonfigurasjon, write_disposition="WRITE_TRUNCATE"
            )
            job = bigQueryKlient.load_table_from_dataframe(
                dataframe,
                f"toi-prod-324e.{db_navn.replace('-', '_')}.{tabell}",
                job_config=jobConfig,
            )
            job.result()
            logger.info(f"Har speilet tabell {tabell} til BigQuery")
        except:
            logger.error(f"Kunne ikke speile tabell {tabell} til BigQuery")
            exit(1)

        logger.error(f"Ferdig med speiling av tabeller fra {db_navn}")


# Speiling av kandidat-API
tabeller = {
    "utfallsendring": [],
    "veilkandidat": [],
    "veilkandliste": [],
    "veilkandidatnotat": [],
    "avviksrapportering": [],
    "formidlingavusynligkandidat": [],
    "sending_av_kandidathendelse": [],
}
speiling_db_bq("rekrutteringsbistand-kandidat-pg15", tabeller, bigQueryKlient, logger)

# Speiling av statistikk-API
tabeller = {
    "kandidatliste": [],
    "kandidatutfall": [],
    "stilling": [],
    "tiltak": [],
    "visning_kontaktinfo": [],
}
speiling_db_bq("rekrutteringsbistand-statistikk-pg15", tabeller, bigQueryKlient, logger)

logger.info("Ferdig med speiling av alle tabeller")
