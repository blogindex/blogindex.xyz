#!/usr/bin/env bash
export ADMIN_API_KEY="BLOG-INDEX-PREVIEW-API" 
uvicorn api.main:app --host "0.0.0.0" --log-config ./log.ini