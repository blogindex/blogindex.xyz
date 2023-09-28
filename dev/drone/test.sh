#!/usr/bin/env bash
apt-get update && apt-get -y install postgresql-client | tee $RESULT_LOCATION.txt
export PG_PASS=${DATABASE_DB_PASS}
WAITLOOP=99
loops=0
TIMEDOUT=1
until [ "${WAITLOOP}" = "0" ]; do
    pg_isready -h ${DATABASE_DB_HOST}
    WAITLOOP=$?
    echo "Waiting for database to come up. ~(${loops}/60 seconds)" | tee -a $RESULT_LOCATION.txt
    sleep 1
    ((loops++))
    if [ $loops -ge 60 ]; then
        TIMEDOUT=1
        break
    fi
done
if [ "${TIMEDOUT}" = "0" ]; then
    echo "Database Is Up!!!" | tee -a $RESULT_LOCATION.txt
fi
cd /drone/src | tee -a $RESULT_LOCATION.txt
python -m venv .test | tee -a $RESULT_LOCATION.txt
source .test/bin/activate | tee -a $RESULT_LOCATION.txt
pip install -r requirements.txt | tee -a $RESULT_LOCATION.txt
PYTHONPATH=. pytest -vvv --cov . --cov-report html --capture=tee-sys | tee -a $RESULT_LOCATION.txt

if [ -d "/drone/src/htmlcov" ]; then
    echo "Copying htmlcov to ${RESULT_LOCATION}" | tee -a $RESULT_LOCATION.txt
    mv htmlcov "${RESULT_LOCATION}" | tee -a $RESULT_LOCATION.txt
fi

if [ -d "${RESULT_LOCATION}" ]; then
    echo "results are available at https://results.blogindex.dev/${RESULT_LOCATION}" | tee -a $RESULT_LOCATION.txt
else
    echo "An unknown error has occurred. Coverage Test Results are not available for this test." | tee -a $RESULT_LOCATION.txt
fi