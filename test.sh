export $(grep -v '^#' .env | xargs)
pytest --exitfirst --verbose --failed-first --cov=. --cov-report html