from fastapi import APIRouter
from starlette.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from starlette.config import Config
from authlib.integrations.starlette_client import OAuth, OAuthError
from datetime import datetime
import urllib.parse

from api.config.dependencies import config
from api.helpers.request import pprint_request

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
async def auth(request: Request):
    # Begin building response    
    response  = "<h1>OpenID Connect Test Page</h1>"
    response += "<p>This page is intended for <b>testing purposes only</b>. This route should be disabled when run in production.</p>"  # noqa: E501
    try:
        # Attempt to login to OAuth2
        token = await oauth.openid.authorize_access_token(request)
        user = token.get('userinfo')
        access_token = token.get('access_token')
    except OAuthError as e:
        
        error_msg = e if e else "Undefinded OAuthError"
        error = {"detail": error_msg}
        response +=  "<div><p style='margin-left:1em;color:red;font-weight:bold;'>"
        response += f"<b>ERROR:</b> {error['detail']}"
        response +=  "</p></div>"
        response +=  "<div><p>"
        response += f"<a href='{request.url_for('login')}'><button>Login</button></a>"
        response +=  "</p></div>"
        response += await pprint_request(request, html=True)
        return HTMLResponse(response)
    response += f"<div><p><a href='{request.url_for('logout')}'><button>Logout</button></a></p>"
    for key in user:
        if key in ["email","name","preferred_username","groups"]:
            if key == "groups":
                response += f"<div>{key}: <pre>"
                for value in user['groups']:
                    response += f"{value}<br/>"
                response += "</pre></div>"
            else:
                response += f"<div>{key}: <pre>{user[key]}</pre></div>"
    response += f"<div><pre>issued: {datetime.utcfromtimestamp(user['auth_time'])}</pre></div>"  # noqa: E501
    response += f"<div><pre>expires: {datetime.utcfromtimestamp(user['exp'])}</pre></div>"  # noqa: E501
    response += "</div>"
    response += "<div style='margin:0.5em;'>"
    response += "<h3>Access Token:</h3>"
    response += "<p>This token is the bearer token used for authentication with the api.<br/>"  # noqa: E501
    response += "You can use this to authenticate using the 'Authorize' button in the "
    response += "<a href='/docs' target='_blank'>API's Swagger UI Documentation</a>.</p>"  # noqa: E501
    response += "<p style='margin:0.25em;'>"
    response += "<button onclick='copy_token()'>Copy Access Token</button>"
    response += "<span style='margin-left:1em;color:red;font-weight:bold;' id='whiteboard'></span></p>"  # noqa: E501
    response += f"<textarea id='token'style='height:25em;width:80%;margin:auto;'>{access_token}</textarea></div>"  # noqa: E501
    response += "<script>function copy_token(){"
    response += "let access_token=document.getElementById('token').value;"
    response += "navigator.clipboard.writeText(access_token);"
    response += "whiteboard = document.getElementById('whiteboard');"
    response += "whiteboard.innerHTML='Copied to Clipboard';"
    response += "setTimeout(()=> {"
    response += "whiteboard.innerHTML='';},3000);"
    response += "}</script>"
    response += await pprint_request(request, html=True)
    return HTMLResponse(response)

@router.get('/login')
async def login(request: Request):
        redirect_uri = request.url_for('auth')
        return await oauth.openid.authorize_redirect(request, redirect_uri)

@router.get('/logout')
async def logout(request: Request):
        request.session.pop('user', None)
        return RedirectResponse(request.url_for('auth'))
