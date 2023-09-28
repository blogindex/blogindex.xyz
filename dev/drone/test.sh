#!/usr/bin/env bash
apt-get update && apt-get -y install postgresql-client
export PG_PASS=${DATABASE_DB_PASS}
WAITLOOP=99
loops=0
until [ "${WAITLOOP}" = "0" ]; do
    pg_isready -h ${DATABASE_DB_HOST}
    WAITLOOP=$?
    echo "Waiting for database to come up. ~(${loops}/60 seconds)"
    sleep 1
    ((loops++))
    if [ $loops -ge 60 ]; then
        break
    fi
done

cd /drone/src
python -m venv .test
source .test/bin/activate
pip install -r requirements.txt
PYTHONPATH=. pytest --exitfirst -vv --cov . --cov-report html

if [ -d "/drone/src/htmlcov" ]; then
    echo "Copying htmlcov to ${RESULT_LOCATION}"
    mv htmlcov "${RESULT_LOCATION}"
fi
