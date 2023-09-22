import os
import jwt
from configparser import ConfigParser
from fastapi import Response, status, HTTPException

def authenticate(token,config):
    if VerifyToken(token,config).verify().get("status"):
        raise HTTPException(status_code=400, detail="Not Authenticated")

class VerifyToken():
    def __init__(self,token,config):
        self.token = token
        self.config = config

        # Gets the JWKS from given url and does processing so you can use any of the keys available
        jwks_url = f'https://{self.config["AUTH0"]["DOMAIN"]}/.well-known/jwks.json'
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
                algorithms = self.config["AUTH0"]["ALGORITHMS"],
                audience = self.config["AUTH0"]["API_AUDIENCE"],
                issuer = self.config["AUTH0"]["ISSUER"]
            )
        except Exception as e:
            return {"status": "error", "msg": str(e)}
        
        return payload