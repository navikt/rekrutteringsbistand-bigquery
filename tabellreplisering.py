import dataverk as dv
from google.cloud import bigquery
from dataverk_vault import api as vault_api
from google.oauth2 import service_account
import psycopg2 as pg
import pandas.io.sql as psql
import logging

logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger("tabellreplisering.py")

# Konfigurasjon av bigQuery-klient
secrets = vault_api.read_secrets()

creds = secrets.pop("GCP_json")
logger.info("Creds: " + str(len(creds)))

credentials = service_account.Credentials.from_service_account_info(eval(creds))
#bigQueryClient = bigquery.Client(credentials=credentials)


jobConfig = bigquery.LoadJobConfig(
    write_disposition="WRITE_TRUNCATE"
)

# Konfigurer lesing fra database
rekrutteringsbistand_creds = secrets["rekrutteringsbistand-kandidat-db-url"]
adeo, ip, creds_loc = rekrutteringsbistand_creds.split(":")
user, password = vault_api.get_database_creds(creds_loc).split(":")
logger.info("DB-brukernavn: " + user)
connection = pg.connect(f"host={adeo} dbname=rekrutteringsbistand-kandidat user={user} password={password}")

tabeller = ["utfallsendring", "veilkandidat", "veilkandliste"]

for tabell in tabeller:
    sql = "select * from " + tabell
    dataframe = psql.read_sql(sql, connection)
    dataframe.to_gbq("kandidat_api." + tabell, credentials=credentials)
    logger.info("Dataframe-kolonner: " + dataframe.columns)
    #job = bigQueryClient.load_table_from_dataframe(dataframe, "toi-prod-324e.kandidat_api." + tabell, job_config=jobConfig)
    #job.result()

exit(0)

# df = dv.read_sql(connector='postgres', source='rekrutteringsbistand-kandidat', sql=sql)

# bq_client = bigquerry.client(credentials=creds)

# job_config = bigquery.LoadJobConfig(
#     # Alle kolonner vil bli skrevet til tabellen, men eksplisitt spesifisering vil sørge for riktig typesetting.
#         bigquery.SchemaField("kandidatliste_uuid", bigquery.enums.SqlTypeNames.STRING),
#         bigquery.SchemaField("kandidatliste_opprettet", bigquery.enums.SqlTypeNames.DATETIME),
#         bigquery.SchemaField("første_kandidat_presentert", bigquerry.enums.SqlTypeNames.DATETIME)
#     ],
#     # Optionally, set the write disposition. BigQuery appends loaded rows
#     # to an existing table by default, but with WRITE_TRUNCATE write
#     # disposition it replaces the table with the loaded data.
#     write_disposition="WRITE_TRUNCATE",
# )

# job = bq_client.load_table_from_dataframe(df, table_id, job_config=job_config)  # Make an API request.
# job.result()  # Venter på at jobben blir ferdig