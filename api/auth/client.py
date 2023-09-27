import http.client
import json


def get_key(domain,audience,client_id,client_secret) -> dict:
    conn = http.client.HTTPSConnection(domain)

    headers = {'content-type': "application/json"}
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": audience,
        "grant_type": "client_credentials"
    }
    json_payload = json.dumps(payload)
    conn.request("POST", "/oauth/token", json_payload, headers)

    resp = conn.getresponse()
    credentials = resp.read().decode("utf-8")
    credentials = json.loads(credentials)
    if isinstance(credentials, dict) and "access_token" in credentials:
        return credentials["access_token"]
    
    return {}


if __name__ == "__main__":
    from os import environ
    creds = {}
    for var in [
                 "AUTH0_DOMAIN",
                 "AUTH0_API_AUDIENCE",
                 "AUTH0_CLIENT_ID",
                 "AUTH0_CLIENT_SECRET"
            ]:
        if var in environ:
            creds[var] = environ[var]
        else:
            raise NameError
    key = get_key(
            creds["AUTH0_DOMAIN"],
            creds["AUTH0_API_AUDIENCE"],
            creds["AUTH0_CLIENT_ID"],
            creds["AUTH0_CLIENT_SECRET"]
            )
    print(key,end="")