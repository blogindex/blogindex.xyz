from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database definition to be used in path functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post(  "/users/create/", response_model=schemas.User)
def create_user(
            user: schemas.UserCreate,
            db: Session = Depends(get_db)
            ):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    print(user.__dict__)
    return crud.create_user(db=db, user=user)

@app.post("/sites/create/", response_model=schemas.Site)
def create_site(
            user_id: int,
            site:schemas.SiteCreate,
            db: SessionLocal = Depends(get_db)
            ):
    return crud.create_site(user_id,site,db)

@app.post("/posts/create/", response_model=schemas.Post)
def create_post(
            page_id: int,
            site:schemas.PostCreate,
            db: SessionLocal = Depends(get_db)
            ):
    return crud.create_post(post_id,post,db)

@app.get("/users/get/all/", response_model=list[schemas.User])
def read_users(
            skip: int = 0,
            limit: int = 100,
            db: Session = Depends(get_db)
            ):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/get/{user_id}/", response_model=schemas.User)
def read_user_by_id(
            user_id: int,
            db: Session = Depends(get_db)
            ):
    user = crud.get_user(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/sites/get/all/", response_model=list[schemas.Site])
def get_sites(
            db: Session = Depends(get_db),
            skip: int = 0,
            limit: int = 10
            ):
    sites = crud.get_sites(db, skip=skip, limit=limit)
    return sites

@app.get("/sites/get/{user_id}/")
def get_sites_by_user_id(
            user_id: int,
            db: Session = Depends(get_db),
            skip: int=0,
            limit: int=10
            ):
    sites = crud.get_sites_by_user_id(
                db,
                user_id=user_id,
                skip=skip,
                limit=limit
                )
    return sites

@app.get("/posts/get/all", response_model=list[schemas.Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts
