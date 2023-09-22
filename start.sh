#!/usr/bin/env bash
export $(grep -v '^#' .env | xargs)
uvicorn api.main:app --host "0.0.0.0" --log-config ./log.ini
