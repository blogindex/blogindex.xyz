#!/usr/bin/env bash
export BLOGINDEX_API_KEY_ADMIN="aaaa-aaaa-aaaa" 
uvicorn api.main:app --host "0.0.0.0" --log-config ./log.ini