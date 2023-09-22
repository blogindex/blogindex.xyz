export $(grep -v '^#' .env | xargs)
export $(grep -v '^#' .testkey | xargs)
echo "TEST_KEY=${TEST_KEY}"
pytest