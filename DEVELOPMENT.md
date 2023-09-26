# Development

## Bring up a development environment

### Docker

Instructions for bringing up a postgres database via docker will go here

### Nix

If you're running nix you can use the development config provided in [dev/nix](dev/nix) to bootstrap everything.

```sh
nix develop # Evoke development shell
./start.sh # Start the app
```

### Test

Automated tests can be run using the docker containers defined in /dev/test  Please see [TESTING.md](TESTING.md) for more information