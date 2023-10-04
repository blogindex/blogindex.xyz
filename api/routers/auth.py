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
    except OAuthError:
        return RedirectResponse("/auth/")
    
    user = token.get('userinfo')
    access_token = token.get('access_token')
    response  = "<h1>OpenID Connect Test Page</h1>"
    response += "<p>This page is intended for <b>testing purposes only</b>. This route should be disabled when run in production.</p>"
    response += f"<div><p><a href='{request.url_for('logout')}'>Logout</a></p>"
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
    response += "</div>"
    response += "<div style='margin:0.5em;'>"
    response += "<h3>Access Token:</h3>"
    response += "<p>This token is the bearer token used for authentication with the api.<br/>"
    response += "You can use this to authenticate using the 'Authorize' button in the "
    response += "<a href='/docs' target='_blank'>API's Swagger UI Documentation</a>.</p>"
    response += "<p style='margin:0.25em;'>"
    response += "<button onclick='copy_token()'>Copy Access Token</button>"
    response += "<span style='margin-left:1em;color:red;font-weight:bold;' id='whiteboard'></span></p>"
    response += f"<textarea id='token'style='height:25em;width:80%;margin:auto;'>{access_token}</textarea></div>"
    response += "<script>function copy_token(){"
    response += "let access_token=document.getElementById('token').value;"
    response += "navigator.clipboard.writeText(access_token);"
    response += "whiteboard = document.getElementById('whiteboard');"
    response += "whiteboard.innerHTML='Copied to Clipboard';"
    response += "setTimeout(()=> {"
    response += "whiteboard.innerHTML='';},3000);"
    response += "}</script>"

    return HTMLResponse(response)
