#!/usr/bin/env bash

apt-get update && apt-get -y install postgresql-client
loops=0
export PG_PASS=${DATABASE_DB_PASS}
until [ "$(pg_isready -h ${DATABASE_DB_HOST} -U ${DATABASE_DB_USER} -d ${DATABASE_DB})" = "0" ] || [ loops = "120" ]; do

    echo "Waiting for database to come up. ~(${loops}/120 seconds)"
    sleep 1
    ((loops++))
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
