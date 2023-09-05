from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from fastapi.exceptions import ResponseValidationError

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session,user: schemas.UserCreate):
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, display=user.display, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_sites(db: Session, skip: int = 0, limit: int = 100):
    try:
        return_value = db.query(models.Site).offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=400, detail="Hmm, something went wrong. Please check the logs.")
    try:
        return return_value
    except error as e:
        raise HTTPException(status_code=400, detail=e)

def get_sites_by_user_id(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 10
    ):
    try:
        return_value = db.query(models.Site).filter(models.User.id == user_id).offset(skip).limit(limit).all()
    except:
        raise HTTPException(status_code=400, detail="Hmm, something went wrong. Please check the logs.")
    try:
        return return_value
    except error as e:
        raise HTTPException(status_code=400, detail=e)


def create_site(
            user_id: int,
            site: schemas.SiteCreate,
            db: Session
            ):
    try:
        db_site = models.Site(**site.dict())
        db.add(db_site)
        db.commit()
        db.refresh(db_site)
        return db_site
    except IntegrityError:
        db.rollback()
        raise HTTPException(
                    status_code=400,
                    detail=f"User with id: {user_id} not found"
        )

def create_post(
            site_id: int,
            post: schemas.PostCreate,
            db: Session
            ):
    try:
        db_post = models.Post(**post.dict())
        db.add(db_post)
        db.commit()
        db.refresh(db_post)
        return db_post
    except IntegrityError:
        db.rollback()
        raise HTTPException(
                    status_code=400,
                    detail=f"Site with id: {post_id} not found"
        )




def get_posts(db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    return_value =  db.query(models.Post).offset(skip).limit(limit).all()
    return return_value