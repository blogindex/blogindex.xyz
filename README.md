# theblogindex.org API

## What is The Blog Index?

A Value 4 Value Blogging Community being built from scratch

# WARNING: UNDER HEAVY DEVELOPMENT

Currently there is heavy development on the API using FastAPI

## How to help

At this point, there is heavy coordination going on off GitHub on Matrix.

Join us in the [blogindex Matrix Space](https://matrix.to/#/#blogindex.xyz:matrix.org) to coordinate development efforts.

Once we get into a more stable, usable state, more will be coordinated on GitHub.

## Local Development

### Database

A docker compose file is created for convenience to automatically set up
a local database and initialise it.

```sh
docker compose up -d
```

### Nix

If you're running nix you can use the provided development config to bootstrap everything.

```sh
nix develop # Evoke development shell
./start.sh # Start the app
```

### Other Environments

The following dependencies need to be installed:

- python3
- postgres
- mariadb-connector-c

You can then run the following commands:

```sh
mkdir -p logs # Ensure a folder exists to write logs
python -m venv .venv # Create python virtual env
source .venv/bin/activate # Active the env
pip install -r requirements.txt # Install the requirements
./start.sh # Start the app
```

### Testing

Once you have the api running correctly, you can test it's functioning by running the tests in a separate shell.

```sh
./test.sh
```
