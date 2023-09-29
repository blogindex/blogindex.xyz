# Development

## Bring up a development environment

### Install Prerequisites
#### Ubuntu / Debian
```
sudo apt-get update
sudo apt-get install -no-install-recommends -y python3.11 python3.11-venv python3.11-pip python3.11-dev libpq-dev build-essential git
```

### Clone Repo
```
git clone https://github.com/blogindex/blogindex.xyz
```

### Create a virtual environment and install requirements
```
cd blogindex.xyz
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Nix

If you're running nix you can use the development config provided in [dev/nix](dev/nix) to bootstrap everything.

```sh
nix develop # Evoke development shell
./start.sh # Start the app
```

## Testing

Automated tests can be run using the docker containers defined in [blogindex/ci-tools](https://github.com/blogindex/ci-tools)

## Deploying with docker

See [dev/docker/deploy](dev/docker/deploy) for a docker-compose file to deploy the app for testing