import os
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from api.config.dependencies import config, token_auth_scheme
from api.auth.bearer import authenticate


router = APIRouter(
        prefix="/logs",
        tags = ["logs"],
        responses={404: {"description": "Not found"}}
)

@router.get('/')
async def logs(
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    with open(os.path.join(app.root_path, "logs", "blogindex.dev")) as log_file:
        log_contents = log_file.read()
        return log_contents

@router.get('/html', response_class=HTMLResponse)
async def logs_html(
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    with open(os.path.join(app.root_path, "logs", "blogindex.dev")) as log_file:
        log_contents = log_file.read().replace('\n','<br>')
        return f"<html><head><meta name='robots' content='noindex'></head><body><div style='position: -webkit-sticky; position: sticky; top:0; padding:1em;'><button onCLick='location.reload()'>Refresh Logs</button></div><div style='padding-top:1em;font-family:courier;'>{log_contents}</div></body></html>"  # noqa: E501
