FROM python:3.11.5-bullseye

RUN apt-get update && \
    apt-get -y --no-install-recommends install \
            git \
            postgresql-client

COPY start /start

ENTRYPOINT /start