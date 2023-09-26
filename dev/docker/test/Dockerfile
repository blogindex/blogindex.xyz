# Test Environment for BlogIndex API using Python 3.11
FROM python:3.11.5-bullseye

RUN apt-get update && apt-get -y install wget git && \
    git clone https://github.com/blogindex/blogindex.xyz/

COPY test /test

WORKDIR /blogindex.xyz

ENTRYPOINT sleep 10 && /test
