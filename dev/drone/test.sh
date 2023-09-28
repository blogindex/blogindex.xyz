#!/usr/bin/env bash

apt-get update && apt-get -y install postgresql-client
loops=0
export PG_PASS=${DATABASE_DB_PASS}
DB_WAIT=99
until [ "DB_UP" = "0" ]; do
    DB_WAIT=$(pg_isready -d ${DATABASE_DB} -h ${DATABASE_DB_HOST} -U ${DATABASE_DB_USER})
    echo "Waiting for database to come up. ~(${loops}/30 seconds) pg_isready exit_code=${DB_UP}"
    sleep 1
    ((loops++))
    if [ loops -gt 29 ]; then
        DB_WAIT=0
    fi
done

cd /drone/src
python -m venv .test
source .test/bin/activate
pip install -r requirements.txt
pytest --exitfirst --verbose --failed-first --cov . --cov-report html

if [ -d "/drone/src/htmlcov" ]; then
    echo "Copying htmlcov to ${RESULT_LOCATION}"
    mv htmlcov "/results/${RESULT_LOCATION}"
fi
sleep 300
