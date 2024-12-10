# Rekrutteringsbistand-bigquery

Applikasjonen kjører periodisk NAIS-jobb for å sende data til GCP BigQuery fra databaser i FSS som tilhører Rekrutteringsbistand-applikasjoner. Dette er unødvendig for data som allerede ligger i GCP.

Data som lastes til GCP BigQuery brukes til å kunne publisere datapakker og datafortellinger til https://data.ansatt.nav.no/ og til å lage dashboard for Rekrutteringsbistand (https://metabase.ansatt.nav.no/).

NB: Applikasjonen kan deaktiveres fra periodisk kjøring ved å kommentere ut "schedule"-parameteren i nais.yaml.

# Hvordan legge til lesing av ny database

## Konfigurasjon
* Gi applikasjonen tilgang til å lese databasen ved å legge inn databasen i [konfigurasjonsfila for rekrutteringsbistand-bigquery](https://github.com/navikt/vault-iac/blob/master/terraform/teams/toi/apps/rekrutteringsbistand-bigquery.yaml) i  vault-iac
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
* Dette Git-repositoriet eies av [team Toi](https://teamkatalog.nav.no/team/76f378c5-eb35-42db-9f4d-0e8197be0131).
* Slack: [#arbeidsgiver-toi-dev](https://nav-it.slack.com/archives/C02HTU8DBSR)

## For folk utenfor Nav
* IT-avdelingen i [Arbeids- og velferdsdirektoratet](https://www.nav.no/no/NAV+og+samfunn/Kontakt+NAV/Relatert+informasjon/arbeids-og-velferdsdirektoratet-kontorinformasjon)
