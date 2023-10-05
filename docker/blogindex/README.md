# Development / Testing
## Required Services
---
### Traefik
---
We use traefik for load balancing / reverse proxy.
Some examples of how to setup [traefik](https://traefik.io/):
- [https://beardedtek.org/traefik-tailscale-linode-dns/](https://beardedtek.org/traefik-tailscale-linode-dns/)
- [https://www.smarthomebeginner.com/traefik-docker-compose-guide-2022/](https://www.smarthomebeginner.com/traefik-docker-compose-guide-2022/)
- [https://medium.com/@containeroo/traefik-2-0-docker-a-simple-step-by-step-guide-e0be0c17cfa5](https://medium.com/@containeroo/traefik-2-0-docker-a-simple-step-by-step-guide-e0be0c17cfa5)

### Authentik
---
For development and testing, we need to first deploy [Authentik](https://goauthentik.io) via docker.  Instructions to do so are in [docker/authentik](/docker/authentik/).

I created a [YouTube Playlist](https://youtube.com/playlist?list=PLOysr0TLQWGTEjsSdQ9HNktWtmyCHIEE0&si=XO8n0M03l4qLMmYr) containing videos I found relevant.  The documentation is a bit hard to follow, but these videos really nail the basics down.

#### Installation
Follow the Installation instructions located at [https://goauthentik.io/docs/installation/docker-compose](https://goauthentik.io/docs/installation/docker-compose) to deploy your own instance.


### Main Stack
---
#### Database
We use [postgres:16.0](https://hub.docker.com/layers/library/postgres/16.0/images/sha256-4c0bc0755f1c8269d218811689a59cde339afe35ffbb3279c4d40a92049b0a49?context=explore) for the API database.

#### API
We use a custom built docker image based on [python:3.12-bullseye](https://hub.docker.com/layers/library/python/3.12-bullseye/images/sha256-96b48a3b2ee571a9e2a184cb15cdf07819f5f57b7d615bbf421cedd90aafbd9f?context=explore) to deploy our FastAPI based api.  See [Dockerfile](Dockerfile) for further details.

This image will clone the branch defined with the environment variable `BLOGINDEX_BRANCH` located in [sample-env/devel`](sample-env/devel)

### Setup
---
#### Directory Structure
The directory structure should look like this:
```
+-- .env          <-- environment variable directory
|    +- api       <-- API Specific
|    +- auth      <-- OAuth / Open ID Connect
|    +- database  <-- Database
|    +- devel     <-- Development Specific **DO NOT INCLUDE IN PRODUCTION!**
|    +- uvicorn   <-- Uvicorn specific
|
+-- data          <-- optional data directory.  Not necessary for development
|    +- postgres
|
+-- docker-compose.yml
+-- Dockerfile
+-- start         <-- Container Entrypoint script
```

### Environment Variables
Copy the sample-env directory to .env
```
cp -r sample-env .env
```
Edit the environment variables to suit your environment:
#### api:
`BLOGINDEX_LOG_LEVEL="DEBUG"` Sets Log Level for uvicorn - SEE logs.

`BLOGINDEX_DEBUG="True"` Sets `DEBUG` mode which will enable a few extra features for debugging. - SEE debugging

`API_DOMAIN=api.mydomain.org` Sets domain used for Traefik reverse-proxy.

#### auth:
`AUTH_CONF_URL="https://authentik.mydomain.org/application/o/blogindex-oauth/.well-known/openid-configuration"` OpenID Connect configuration URL

`AUTH_JWKS_URL="https://authentik.mydomain.org/application/o/blogindex-oauth/jwks/"` OAuth2 / OpenID Connect jwks.json endpoint

`AUTH_ISSUER="https://authentik.mydomain.org/application/o/blogindex-oauth/"` OAuth2 / OpenID Connect Issuer

`AUTH_CLIENT_ID="YourClientID"` CLIENT_ID from OAuth2 / OpenID Connect Provider ***NOTE:*** Also used as AUDIENCE when using Authentik

`AUTH_CLIENT_SECRET="YourClientSecret"` CLIENT_SECRET from OAuth2 / OpenID Connect Provider

`AUTH_ALGORITHMS="RS256"` OAuth2 / OpenID Connect Provider Algorithm

#### database:
`DATABASE_DB="blogindex"` Postgres Database Name

`DATABASE_DB_HOST="apidb"` Postgres hostname

`DATABASE_DB_USER="blogindex"` Postgres User

`DATABASE_DB_PASS="blogindex"` Postgres Password

#### devel:
`BLOGINDEX_BRANCH="main"` Tells docker entrypoint script which branch to clone from github

`USE_LOCAL_CODEBASE=true` Tells docker image to create a symbolic link to the local codebase from /blogindex

`LOCAL_CODEBASE=/path/to/local/codebase` MUST be set if you set `USE_LOCAL_CODEBASE` to `true`.  Defines host path of local codebase

#### uvicorn:
Any uvicorn environment variable can be added to this file, but this is what we are currently using.
A list of settings can be found at [https://www.uvicorn.org/settings/](https://www.uvicorn.org/settings/).

`UVICORN_HOST="0.0.0.0"` Set to `0.0.0.0` to listen on all interfaces

`UVICORN_LOG_CONFIG="./log.ini"` This should not change as it is part of the repository

`UVICORN_PROXY_HEADERS=True` equivalent of --proxy-headers

`FORWARDED_ALLOWED_IPS="*"` Comma separated list of IPs to trust with proxy headers

### docker networks
---
We use traefik for reverse-proxying and need an network for traefik to use docker labels for configuration.

```
docker network create traefik
```

Since we want the database to communicate with only blogindex services, we will create a blogindex network as well.

```
docker network create blogindex-dev
```

### docker-compose.yml
---
This is the development docker-compose.yml file.

```
---
version: '3'

networks:
  traefik:
    external: true
  blogindex-dev:
    external: true

services:

  api:
    container_name: api
    build: .
    image: blogindex/api:main
    volumes:
      # Set to true in .env/devel to use a local codebase
      - ${LOCAL_CODEBASE:-./blogindex}:/local
      # Used by /blogindex/start.sh to import environment variables.
      - .env:/blogindex/.env:ro
    depends_on:
      - apidb
    environment:
      - USE_LOCAL_CODEBASE=${USE_LOCAL_CODEBASE:-false}
    env_file:
      - .env/devel
    networks:
      - traefik
      - blogindex
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`${API_DOMAIN:-api.mydomain.org}`)"
      - "traefik.http.routers.api.entryPoints=https"
      - "traefik.http.routers.api.tls=true"
      - "traefik.http.routers.api.tls.certresolver=le"
      - "traefik.http.routers.api.service=api-entrypoint"
      - "traefik.http.services.api-entrypoint.loadbalancer.server.port=8000"
  
  apidb:
    container_name: apidb
    hostname: ${DATABASE_DB_HOST:-db}
    image: postgres
    restart: always
    environment:
      - POSTGRES_USER=${DATABASE_DB_USER:-blogindex}
      - POSTGRES_PASSWORD=${DATABASE_DB_PASS:-blogindex}
      - POSTGRES_DB=${DATABASE_DB:-blogindex}
    env_file:
      - .env/database
    networks:
      - blogindex
```

### Build the api image
Included in the compose file is a reference to build the container.  At this time it is not available on docker hub or GitHub Container Registry, so this is the only option.

Docker Version 3.2.1 and up:
```
docker compose build
```

Standalone docker-compose:
```
docker-compose build
```

### Bring it up
Docker Version 3.2.1 and up:
```
docker compose up -d
```

Standalone docker-compose:
```
docker compose up -d
```

### View the Logs
Docker Version 3.2.1 and up:
```
docker compose logs -f
```

Standalone docker-compose:
```
docker-compose logs -f
```

### Test it out
1. Visit `https://api.mydomain.org/auth/`
2. Click Login to authenticate and obtain an access_token.
3. Click `Copy Token` button to copy token to the clipboard
4. Visit `https://api.mydomain.org/docs`
5. Click `Authorize` button at the top left of the page
6. Enter `access_token` obtained in step 3into the `HTTPBearer` field
7. Click `Authorize`
8. Click `Close`
9. Expand an endpoint, `/author/get/all` for example
10. Click `Try It Out` button
11. Click `Execute`

You should get a response from the server if it all was setup properly.  If you are getting status_code 400 {"detail": "Not Authenticated"} there is an issue with your authentication setup.

### Current Development Version
The current development version of the api will be available at {https://preview.blogindex.dev}(https://preview.blogindex.dev).  If it is down, that means the current development version is currently broken.  If that's the case, feel free to reach out and let us know.