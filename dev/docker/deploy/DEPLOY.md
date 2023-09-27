# Deploy API for Development

Using docker, you can stand up the app using either a branch of the repository or a local codebase for manual testing.
By design it completely destroys the environment each time you stop the container so that all scripts, setup and teardown function just like you're setting it up the first time.

## Configuration
### Obtain Auth0 Credentials
Obtain a copy of the credentials from @beardedtek:matrix.org or sign up for Auth0 at [https://auth0.com](https://auth0.com) and obtain your own test credentials.

Further instructions will be written within the next week or so.

### copy example.env to .env and modify its contents
```sh
cp example-env .env
nano .env
```

*example.env*
```
# Local Codebase Config
USE_LOCAL_CODEBASE=false
LOCAL_CODEBASE=/path/to/local/codebase

# Log Level Config
BLOGINDEX_LOG_LEVEL="DEBUG"

# Database Config
DATABASE_DB="blogindex"
DATABASE_DB_HOST="db"
DATABASE_DB_USER="blogindex"
DATABASE_DB_PASS="blogindex"
BLOGINDEX_DEBUG="True"

# The following variables can be obtained by messaging @BeardedTek:matrix.org
# You can create your own instance of Auth0 for an API at https://auth0.com
AUTH0_DOMAIN=""
AUTH0_API_AUDIENCE=""
AUTH0_ISSUER="h"
AUTH0_ALGORITHMS=""
```

### Build the container
```
docker compose build
```

### Bring it up
```
docker compose up
```

### Play around with the API
The api will be at `http://localhost:8000` and can be easily be interacted with at `http://localhost:8000/docs`

### LOGS
Logs can be viewed from the command line
```
docker compose logs -f
```

### Tear it down
```
docker compose down
```