import dataverk as dv
from google.cloud import bigquerry
dv = Client()

tabeller = ["utfallsendring", "veilkandidat", "veilkandliste"]

for tabell in tabeller:
    sql = "select * from " + tabell
    df = dv.read_sql(connector='postgres', source='rekrutteringsbistand-kandidat', sql=sql)
    print("Hentet data fra databasetabell " + tabell)


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