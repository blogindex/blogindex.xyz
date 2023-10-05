# Deploying

## Requirements
In order to bring the app, the following services need to run:
- Authentik
- Postgres 15

## Authentik
Authentik is an open-source Identity Provider focused on flexibility and versatility.

We are using it as a OAuth2 / OpenID Connect provider.

Further documentation and instructions to deploy in our configurtaion are provided in [docker/authentik](docker/authentik).

## Postgres 16
We use the [postgres:16.0](https://hub.docker.com/layers/library/postgres/16.0/images/sha256-4c0bc0755f1c8269d218811689a59cde339afe35ffbb3279c4d40a92049b0a49?context=explore) docker image to provide a database for the API.

Further documentation and instructions to deploy in our configuration are provided in [docker/blogindex](docker/blogindex).

## api.theblogindex.org
We use a custom built docker image based on [python:3.12-bullseye](https://hub.docker.com/layers/library/python/3.12-bullseye/images/sha256-96b48a3b2ee571a9e2a184cb15cdf07819f5f57b7d615bbf421cedd90aafbd9f?context=explore) to deploy our FastAPI based api.

Further documentation and instructions to deploy in our configuration are provided in [docker/blogindex](docker/blogindex).
