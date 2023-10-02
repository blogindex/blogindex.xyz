from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api import crud, schemas
from api.auth.bearer import authenticate
from api.config.dependencies import config, get_db, token_auth_scheme


router = APIRouter(
        prefix="/author",
        tags = ["author"],
        responses={404: {"description": "Not found"}}
)

@router.post(
        "/create",
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

@router.get("/get/all", response_model=list[schemas.Author])
async def get_all_authors(
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    authors = crud.get_all_authors(db, skip=skip, limit=limit)
    return authors

@router.get("/get/by-email/", response_model = list[schemas.Author])
async def get_authors_by_email(
        email: str,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    author = crud.get_author_by_email(email, db)
    return author

@router.get("/get/by-id/", response_model = list[schemas.Author])
async def get_author_by_id(
        id: int,
        db: Session = Depends(get_db),
        token: str = Depends(token_auth_scheme)
        ):
    authenticate(token.credentials,config)
    author = crud.get_author_by_id(id, db)
    return author