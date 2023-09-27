from os import environ
from pprint import pprint
import sys
from api.auth.client import get_key

credentials = {
            "TYPE": "CLIENT"
}
points = 0
for var in environ:
    if var in environ:
        if var == "TEST_KEY":
            points = 4
            credentials["TYPE"] = "KEY"
            credentials["KEY"] = environ[var]
        elif "AUTH0_CLIENT_ID" in var:
            credentials["CLIENT_ID"] = environ[var]
            points += 1
        elif "AUTH0_CLIENT_SECRET" in var:
            credentials["CLIENT_SECRET"] = environ[var]
            points += 1
        elif "AUTH0_DOMAIN" in var:
            credentials["DOMAIN"] = environ[var]
            points += 1
        elif "AUTH0_API_AUDIENCE" in var:
            credentials["AUDIENCE"] = environ[var]
            points += 1

if points < 4:
    msg = "You must set either TEST_KEY or BOTH CLIENT_ID and CLIENT_SECRET environment variables"
    sys.exit(msg)
elif points > 4:
    msg = "You cannot set both TEST_KEY and CLIENT_ID/CLIENT_SECRET.  Pick one."
    sys.exit(msg)

if credentials["TYPE"] == "CLIENT":
    credentials["KEY"] = get_key(
                credentials["DOMAIN"],
                credentials["AUDIENCE"],
                credentials["CLIENT_ID"],
                credentials["CLIENT_SECRET"]
    )

if __name__ == "__main__":
    print(points)
    pprint(credentials)