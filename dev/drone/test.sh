#!/usr/bin/env bash

cd /drone/src
python -m venv .test
source .test/bin/activate
pip install -r requirements.txt
pytest --exitfirst --verbose --failed-first --cov . --cov-report html

if [ -d "/drone/src/htmlcov" ]; then
    echo "Copying htmlcov to ${RESULT_LOCATION}"
    mv htmlcov "/results/${RESULT_LOCATION}"
fi
    