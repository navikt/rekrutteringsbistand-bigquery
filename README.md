# Rekrutteringsbistand-bigquery

Applikasjonen kjører periodisk NAIS-jobb for å sende data til GCP BigQuery fra databaser i FSS som tilhører Rekrutteringsbistand-applikasjoner. Dette er unødvendig for data som allerede ligger i GCP.

Data som lastes til GCP BigQuery brukes til å kunne publisere datapakker til https://data.intern.nav.no/ og til å lage dashboard for Rekrutteringsbistand (https://metabase.intern.nav.no/).

NB: Applikasjonen kan deaktiveres fra periodisk kjøring ved å kommentere ut "schedule"-parameteren i nais.yaml.

# Hvordan legge til lesing av ny database

## Konfigurasjon
* Gi applikasjonen tilgang til å lese databasen ved å legge inn databasen i [konfigurasjonsfila for rekrutteringsbistand-bigquery](https://github.com/navikt/vault-iac/blob/rekrutteringsbistand-bigquery/terraform/teams/toi/apps/rekrutteringsbistand-bigquery.yaml) i  vault-iac
* Legg til URL for databasen som ny secret i Vault under kv/prod/fss/rekrutteringsbistand-bigquery/toi
* Opprett nytt datasett i [GCP Console](https://console.cloud.google.com) med navngivning som gjenspeiler hvilken applikasjon/database tabellene kommer fra

## Nytt script for å speile tabeller fra ny database
Ta utgangspunkt i et eksisterende script og gjør følgende endringer:
* For databasetilkobling må du:
    * referere til den nye secret'en som er opprettet i Vault
    * endre til riktig databasenavn i tilkoblingsstrengen
* For å speile tabeller til BigQuery må du:
    * spesifisere tabellene i tabell-variabelen
    * spesifisere riktig navn på datasett som tabellene skal speiles til


# Henvendelser

## For Nav-ansatte
* Dette Git-repositoriet eies av [Team tiltak og inkludering (TOI) i Produktområde arbeidsgiver](https://teamkatalog.nais.adeo.no/team/0150fd7c-df30-43ee-944e-b152d74c64d6).
* Slack-kanaler:
    * [#arbeidsgiver-toi-dev](https://nav-it.slack.com/archives/C02HTU8DBSR)
    * [#arbeidsgiver-utvikling](https://nav-it.slack.com/archives/CD4MES6BB)

## For folk utenfor Nav
* Opprett gjerne en issue i Github for alle typer spørsmål
* IT-utviklerne i Github-teamet https://github.com/orgs/navikt/teams/toi
* IT-avdelingen i [Arbeids- og velferdsdirektoratet](https://www.nav.no/no/NAV+og+samfunn/Kontakt+NAV/Relatert+informasjon/arbeids-og-velferdsdirektoratet-kontorinformasjon)
