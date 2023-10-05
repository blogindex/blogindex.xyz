import jwt
from fastapi import HTTPException
from pprint import pprint

from api.config.dependencies import config

def authenticate(token,config):
    auth = VerifyToken(token,config)
    my_auth = auth.verify()
    my_auth_result = my_auth.get("status")
    if my_auth_result:
        raise HTTPException(status_code=400, detail="Not Authenticated")

class VerifyToken():
    def __init__(self,token,config):
        self.token = token
        self.config = config

        # Gets the JWKS from given url
        # Does processing so you can use any of the keys available
        jwks_url = config['AUTH']['JWKS_URL']
        self.jwks_client = jwt.PyJWKClient(jwks_url)

    def verify(self):
        try:
            self.signing_key = self.jwks_client.get_signing_key_from_jwt(
                self.token
            ).key
        except jwt.exceptions.PyJWKClientError as error:
            return {"Status": "error", "msg": error.__str__()}
        except jwt.exceptions.DecodeError as error:
            return {"status": "error", "msg": error.__str__()}


        try:
            payload = jwt.decode(
                self.token,
                self.signing_key,
                algorithms = "RS256",
                issuer = config['AUTH']['ISSUER'],
                audience = config['AUTH']['CLIENT_ID']
            )
        except Exception as e:
            return {"status": "error", "msg": str(e)}
        
        return payload