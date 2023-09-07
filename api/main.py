import logging
from pprint import pprint
from fastapi import Depends, FastAPI, HTTPException, Security
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from os import environ
import os

from . import crud, models, schemas
from .database import SessionLocal, engine
from .helpers.configuration import blogindex, config_schema

blogindex = blogindex()
blogindex.get(config_schema)

models.Base.metadata.create_all(bind=engine)

# Database definition to be used in path functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/logs", StaticFiles(directory="logs"),name="logs")

# Get API Keys
def get_api_keys(api_keys: list = [blogindex.config["API_KEY_ADMIN"]]) -> list:
    db = SessionLocal()
    try:
        keys = db.query(models.Key).all()
        for item in keys:
            api_keys.append(item.key)
    finally:
        db.close()
    return api_keys
api_keys = get_api_keys()

print(api_keys)



# API Key Header Definition
api_key_header = APIKeyHeader(name="X-API-Key")

# API Key Handler
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in api_keys:
        return api_key_header
    raise HTTPException(
            status_code = 401,
            detail = "Invalid or missing API Key"
    )



@app.get('/favicon.ico', response_class=FileResponse)
async def favicon(
        api_key: str = Security(get_api_key)
        ):
    favicon = "favicon.ico"
    favicon_path = os.path.join(app.root_path, "static", favicon)
    return FileResponse(path=favicon_path, headers={"Content-Disposition": "attachment; filename=" + favicon})

@app.get('/logs', response_class=HTMLResponse)
async def logs(
        api_key: str = Security(get_api_key)
        ):
    with open(os.path.join(app.root_path, "logs", "blogindex.dev")) as log_file:
        log_contents = log_file.read().replace('\n','<br>')
        return f"<div style='position: -webkit-sticky; position: sticky; top:0; padding:1em;'><button onCLick='location.reload()'>Refresh Logs</button></div><div style='padding-top:1em;font-family:courier;'>{log_contents}</div>"

@app.get('/', response_class=HTMLResponse)
async def root():
    return RedirectResponse(url="https://blogindex.xyz")

@app.post('/')
async def root_post():
    raise HTTPException(
        status_code = 404
    )

@app.post(
        "/users/create",
        response_model=schemas.User,
        )
async def create_user(
        user: schemas.UserCreate,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    print(f"-------------------\n {user.email}\n ---------------------")
    try:
        user_by_email = crud.get_user_by_email(db, email=user.email)
        if user_by_email:
            raise HTTPException(status_code=400, detail="Email already registered")
        print(f"-------------------\n {user}\n ---------------------")
    except TypeError:
        pass
    return crud.create_user(db=db, user=user)

@app.get("/users/get/all", response_model=list[schemas.User])
async def get_all_users(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_all_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/get/by-email/{email}", response_model = list[schemas.User])
async def get_users_by_email(
        email: str,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_user_by_email(email, db)
    return users

@app.get("/users/get/by-id/{user_id}", response_model = list[schemas.User])
async def get_users_by_id(
        user_id: int,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    users = crud.get_user_by_id(db, id)
    return users


@app.post("/key/create", response_model = list[schemas.KeyDisplay])
async def create_key(
        key: schemas.KeyCreate,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    new_key = crud.create_key(key,db)
    return new_key

@app.get("/key/get/by-user_id/{user_id}", response_model = list[schemas.Key])
async def get_user_keys(
        user_id: int,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    keys = crud.get_user_keys(user_id, db)
    return keys

@app.post("/site/create", response_model = list[schemas.SiteCreate])
def create_site(
        site: schemas.SiteCreate,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    new_site = crud.create_site(db,site)
    return new_site

@app.get("/site/get/all", response_model=list[schemas.Site])
async def get_all_sites(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        api_key: str = Security(get_api_key)
        ):
    sites = crud.get_all_sites(db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-id")
async def get_sites_by_site_id(
        site_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        api_key: str = Security(get_api_key)
        ):
    sites = crud.get_sites_by_site_id(site_id, db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-user_id")
async def get_sites_by_user_id(
        user_id: int,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        api_key: str = Security(get_api_key)
        ):
    sites = crud.get_sites_by_user_id(user_id, db, skip=skip, limit=limit)
    return sites

@app.get("/site/get/by-user_email")
async def get_sites_by_user_email(
        email: EmailStr,
        db: Session = Depends(get_db),
        skip: int = 0,
        limit: int = 100,
        api_key: str = Security(get_api_key)
        ):
    sites = crud.get_sites_by_user_email(email, db, skip=skip, limit=limit)
    return sites

@app.get("/user/exists/by-email")
async def get_user_exists_by_email(
        email: EmailStr,
        db: Session = Depends(get_db),
        json: bool = True
        ):
    return crud.user_exists_by_email(
        email,
        db
        )

@app.get("/user/exists/by-id")
async def get_user_exists_by_id(
        id: int,
        db: Session = Depends(get_db),
        json: bool = True
        ):
    return crud.user_exists_by_id(
        id,
        db,
        json
        )    