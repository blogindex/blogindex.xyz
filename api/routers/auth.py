import logging

from os import environ
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError
from datetime import datetime
from pprint import pprint

from api.config.dependencies import config, get_db, token_auth_scheme
from api.auth.bearer import authenticate

openid_config = Config('.env/blogindex')
oauth = OAuth(openid_config)

oauth.register(
name = 'openid',
server_metadata_url = config['AUTH']['CONF_URL'],
client_kwargs = {
        'scope': 'openid email profile'
}
)

router = APIRouter(
        prefix="/auth",
        tags = ["auth"],
        responses={404: {"description": "Not found"}}
)

@router.get('/')
async def token_home(request: Request):
        login_uri = request.url_for('login')
        return HTMLResponse(f"<a href='{login_uri}'>Login</a>")

@router.get('/login')
async def login(request: Request):
        redirect_uri = request.url_for('get_token')
        return await oauth.openid.authorize_redirect(request, redirect_uri)

@router.get('/logout')
async def logout(request: Request):
        request.session.pop('user', None)
        return RedirectResponse(request.url_for('token_home'))

@router.get('/token/get')
async def get_token(request: Request):
    try:
        token = await oauth.openid.authorize_access_token(request)
    except OAuthError as error:
        pprint(config)
        if config["BLOGINDEX"]["LOG_LEVEL"] == "DEBUG" or config["BLOGINDEX"]["DEVEL"]:
            return {"error": error }
        return {"error": "Error"}
    
    user = token.get('userinfo')
    access_token = token.get('access_token')
    response = f"<div><a href='{request.url_for('logout')}'>Logout</a><div>"
    for key in user:
        if key in ["email","name","preferred_username","groups"]:
            if key == "groups":
                response += f"<div>{key}: <pre>"
                for value in user['groups']:
                    response += f"{value}<br/>"
                response += "</pre></div>"
            else:
                response += f"<div>{key}: <pre>{user[key]}</pre></div>"
    response += f"<div><pre>issued: {datetime.utcfromtimestamp(user['auth_time'])}</pre></div>"
    response += f"<div><pre>expires: {datetime.utcfromtimestamp(user['exp'])}</pre></div>"
    response += f"</div><div>Access Token:<br/><textarea style='height:25em;width:80%;margin:auto;'>{access_token}</textarea></div>"

    return HTMLResponse(response)
