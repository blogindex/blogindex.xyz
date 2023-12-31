from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import EmailStr

from api import crud, schemas
from api.auth.bearer import authenticate
from api.config.dependencies import config, get_db, token_auth_scheme


router = APIRouter(
        prefix="/site",
        tags = ["site"],
        responses={404: {"description": "Not found"}}
)

@router.post("/create", response_model = schemas.Site)
def create_site(
        site: schemas.SiteCreate,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    new_site = crud.create_site(db,site)
    return new_site

@router.get("/get/all", response_model=list[schemas.Site])
async def get_all_sites(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_all_sites(db, skip=skip, limit=limit)
    return sites

@router.get("/get/by-id")
async def get_site_by_site_id(
        id: int,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_site_by_id(id, db)
    return sites

@router.get("/get/by-author_id")
async def get_sites_by_author_id(
        author_id: int,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_sites_by_author_id(author_id, db)
    return sites

@router.get("/get/by-author_email")
async def get_sites_by_author_email(
        author_email: EmailStr,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    sites = crud.get_sites_by_author_email(author_email, db)
    return sites