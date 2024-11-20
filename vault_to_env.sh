#!/bin/sh
if test -f '/secret/rekrutteringsbistand-kandidat-pg15-readonly/username'; then
    export KANDIDAT_USERNAME=$(cat /secret/rekrutteringsbistand-kandidat-pg15-readonly/username)
    echo '- exporting KANDIDAT_USERNAME'
fi

if test -f '/secret/rekrutteringsbistand-kandidat-pg15-readonly/password'; then
    export KANDIDAT_PASSWORD=$(cat /secret/rekrutteringsbistand-kandidat-pg15-readonly/password)
    echo '- exporting KANDIDAT_PASSWORD'
fi

#!/bin/sh
if test -f '/secret/rekrutteringsbistand-statistikk-pg15-readonly/username'; then
    export STATISTIKK_USERNAME=$(cat /secret/rekrutteringsbistand-statistikk-pg15-readonly/username)
    echo '- exporting STATISTIKK_USERNAME'
fi

if test -f '/secret/rekrutteringsbistand-statistikk-pg15-readonly/password'; then
    export STATISTIKK_PASSWORD=$(cat /secret/rekrutteringsbistand-statistikk-pg15-readonly/password)
    echo '- exporting STATISTIKK_PASSWORD'
fi

if test -f '/var/run/secrets/nais.io/vault/GCP_json'; then
    export GCP_JSON=$(cat /var/run/secrets/nais.io/vault/GCP_json)
    echo '- exporting GCP_JSON'
fi