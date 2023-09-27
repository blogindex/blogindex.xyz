from fastapi import APIRouter, Depends, Response

from api.config.dependencies import config, get_db, token_auth_scheme
from api.auth.bearer import authenticate


router = APIRouter(
        prefix="/auth",
        tags = ["auth"],
        responses={404: {"description": "Not found"}}
)

@router.get('/test')
def auth0_test(response: Response, token: str = Depends(token_auth_scheme)):
    authenticate(token.credentials,config)
    logging.debug(token)
    return ({"Verified":True})