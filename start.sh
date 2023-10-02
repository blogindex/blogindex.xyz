#!/usr/bin/env bash

APP_PATH="$(dirname "$(readlink -f "$0")")"
FILES="${APP_PATH}/.env/*"
for f in $FILES; do
    export $(grep -v '^#' ${f} | xargs)
done

uvicorn api.main:app
