import logging
from pprint import pprint
from fastapi import Depends, FastAPI, HTTPException, Security, Response, status
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from os import environ
import os
import sys

from . import crud, models, schemas
from .auth.bearer import VerifyToken
from .auth.bearer import authenticate
from .config.configure import Configure
from .config.database import database

# Configuration
if "BLOGINDEX_DEBUG" not in environ or environ["BLOGINDEX_DEBUG"] != "True":
    sys.tracebacklimit = 0

Config = Configure()
config = Config.get()
dbase = database(config)

models.Base.metadata.create_all(bind=dbase.engine)

# Database definition to be used in path functions
def get_db():
    db = dbase.SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/logs", StaticFiles(directory="logs"),name="logs")

# HTTP Bearer Authentication
token_auth_scheme = HTTPBearer()

@app.get('/auth0/test')
def auth0_test(response: Response, token: str = Depends(token_auth_scheme)):
    authenticate(token.credentials,config)
    logging.debug(token)
    return ({"Verified":True})

@app.get('/logs')
async def logs(
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    with open(os.path.join(app.root_path, "logs", "blogindex.dev")) as log_file:
        log_contents = log_file.read()
        return log_contents

@app.get('/logs/html', response_class=HTMLResponse)
async def logs(
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    with open(os.path.join(app.root_path, "logs", "blogindex.dev")) as log_file:
        log_contents = log_file.read().replace('\n','<br>')
        return f"<html><head><meta name='robots' content='noindex'></head><body><div style='position: -webkit-sticky; position: sticky; top:0; padding:1em;'><button onCLick='location.reload()'>Refresh Logs</button></div><div style='padding-top:1em;font-family:courier;'>{log_contents}</div></body></html>"

@app.post(
        "/author/create",
        response_model=schemas.Author,
        )
async def create_user(
        author: schemas.AuthorCreate,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    try:
        if crud.get_author_by_email(db, email=author.email):
            raise HTTPException(status_code=400, detail="Email already registered")
    except TypeError:
        pass
    return crud.create_author(db=db, author=author)

@app.get("/author/get/all", response_model=list[schemas.Author])
async def get_all_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors

@app.get("/author/get/by-email/", response_model = list[schemas.Author])
async def get_authors_by_email(
        email: str,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    author = crud.get_author_by_email(email, db)
    return author

@app.get("/author/get/by-id/", response_model = list[schemas.Author])
async def get_author_by_id(
        id: int,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    author = crud.get_author_by_id(id, db)
    return author

@app.post("/site/create", response_model = schemas.SiteCreate)
def create_site(
        site: schemas.SiteCreate,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    new_site = crud.create_site(db,site)
    return new_site

@app.get("/site/get/all", response_model=list[schemas.Site])
async def get_all_sites(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_all_sites(db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-id")
async def get_sites_by_site_id(
        site_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_sites_by_site_id(site_id, db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-user_id")
async def get_sites_by_user_id(
        user_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_sites_by_user_id(user_id, db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-user_email")
async def get_sites_by_user_email(
        email: EmailStr,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_sites_by_user_email(email, db, skip=skip, limit=limit)
    return sites