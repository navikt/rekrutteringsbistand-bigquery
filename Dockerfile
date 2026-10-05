FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.14.7-dev AS dev

USER root
RUN apk add --no-cache build-base postgresql-dev

WORKDIR /app

RUN python -m venv venv
ENV PATH="/app/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# psycopg2 bygges fra kilde og trenger libpq (med avhengigheter) når den kjører.
# Runtime-imaget har ikke disse, så vi finner bibliotekene psycopg2 faktisk laster
# og kopierer dem til /app/lib, inkludert symlenkene med soname.
RUN <<EOF
python - <<'PY'
import os
import shutil

GLIBC = ("ld-linux", "libc.so", "libm.so", "libdl.so", "libpthread.so", "librt.so", "libresolv.so")

def lastede_biblioteker():
    with open("/proc/self/maps") as maps:
        stier = {linje.split()[-1] for linje in maps if linje.strip()}
    return {sti for sti in stier if sti.startswith("/") and ".so" in os.path.basename(sti)}

før = lastede_biblioteker()
import psycopg2
nye = {sti for sti in lastede_biblioteker() - før if not sti.startswith("/app/")}

os.makedirs("/app/lib")
for sti in sorted(nye):
    navn = os.path.basename(sti)
    if navn.startswith(GLIBC):
        continue
    shutil.copy2(sti, "/app/lib/" + navn)
    mappe = os.path.dirname(sti)
    for lenke in os.listdir(mappe):
        lenkesti = os.path.join(mappe, lenke)
        if lenke != navn and os.path.islink(lenkesti) and os.path.realpath(lenkesti) == sti:
            os.symlink(navn, "/app/lib/" + lenke)
    print("Kopierer", sti)
PY
EOF

FROM europe-north1-docker.pkg.dev/cgr-nav/pull-through/nav.no/python:3.14.7

WORKDIR /app

COPY --from=dev /app/venv /app/venv
COPY --from=dev /app/lib /app/lib
ENV PATH="/app/venv/bin:$PATH"
ENV LD_LIBRARY_PATH="/app/lib"

RUN ["python", "-c", "import psycopg2; print('psycopg2', psycopg2.__version__, 'libpq', psycopg2.__libpq_version__)"]

COPY speiling_db_bq.py .

ENTRYPOINT ["python", "speiling_db_bq.py"]