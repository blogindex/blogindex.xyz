# Test Environment for BlogIndex API using Python 3.11
FROM python:3.11.5-bullseye

RUN apt-get -y install wget git && \
    git clone https://github.com/blogindex/blogindex.xyz/

COPY test.sh /blogindex.xyz/test.sh

WORKDIR /blogindex.xyz

CMD /usr/bin/env bash /blogindex.xyz/test.sh && sleep 10000


