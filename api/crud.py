from fastapi import HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import EmailStr
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
import logging
import sys

from .helpers.records import author_exists, site_exists, get_author
from . import models, schemas

def create_author(
        db: Session,
        author: schemas.AuthorCreate
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")
    author = models.Author(
                email = author.email,
                first_name = author.first_name,
                last_name = author.last_name,
                display = author.display,
                image = author.image,
                avatar = author.avatar,
                flags = author.flags,
                rating = author.rating,
                disabled = author.disabled,
                value = author.value
    )
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def get_author_by_email(
        email: str,
        db: Session
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")
    author = author_exists(db,email=email)
    if not author:
        raise HTTPException(
            status_code=400,
            detail="no records"
        )
    return [author]

def get_author_by_id(
        author_id: int,
        db: Session
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")
    author = author_exists(db,id=author_id)
    if not author:
        raise HTTPException(
            status_code=400,
            detail="no records"
        )
    return [author]

def get_all_authors(
    db: Session,
    skip: int = 0,
    limit: int = 100
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")
    query = db.query(models.Author).offset(skip).limit(limit) 
    if db.query(query.exists()).first():
        return query.all()
    else:
        raise HTTPException(
            status_code=400,
            detail="no records"
        )


def create_site(
        db:Session,
        site: schemas.SiteCreate
    ):
    """Creates a new site in the database

    Args:
        db (Session): Database Session
        site (schemas.SiteCreate): Pydantic schema to validate model

    Raises:
        HTTPException: 400 URL Exists:
                            No Duplicate URL's Allowed
        HTTPException: 400 User Does Not Exist:
                            Site needs to be attached to a user

    Returns:
        _type_: _description_
    """
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if author_exists(db,id=site.user_id):
        if site_exists(db,url=site.url):
            try:
                user = db.query(models.User).filter(models.User.id == site.user_id).first()  # noqa: E501
                user_info = f"{user.display}:{user.email}"
            except:  # noqa: E722
                user_info = "an unkwnown or deleted user"
            finally:
                raise HTTPException(
                    status_code=400,
                    detail=f"URL already exists and owned by {user_info}.\
                        Please contact support@blogindex.xyz if this is an error."
                )
        else:
            try:
                site = models.Site(
                    url = site.url,
                    name = site.name,
                    description = site.description,
                    flags = site.flags,
                    rating = site.rating,
                    disabled = site.disabled,
                    value= site.value,
                    user_id = site.user_id
                )

                db.add(site)
                db.commit()
                db.refresh(site)
            except ResponseValidationError as error:
                raise HTTPException(
                    status_code=400,
                    detail=f"Validation Error:{error}"
                )
            return site
    else:
        try:
            user_id = db.query(models.Author).filter(models.Author.id == site.user_id).first()  # noqa: E501
        except ProgrammingError:
            raise HTTPException(
                status_code=400,
                detail=f"Author with id: {site.user_id} does not exist.\
                    You must provide a valid Author ID to attach this site to." 
            )
    

def get_all_sites(
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if site_exists(db,all_records=True):
        return db.query(models.Site).offset(skip).limit(limit).all()

    raise HTTPException(
                status_code=400,
                detail="No Sites are in the database." 
                )

def get_site_by_id(
        id: int,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
    
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if site_exists(db,id=id):
        query = db.query(models.Site).filter(models.Site.id == id).offset(skip).limit(limit)  # noqa: E501
        return query.first()

    raise HTTPException(
        status_code=400,
        detail="no records" 
    )

def get_sites_by_author_id(
        user_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if author_exists(db,id=user_id):
        if site_exists(db,user_id=user_id):
            query = db.query(models.Site).filter(models.Site.user_id == user_id).offset(skip).limit(limit)  # noqa: E501
            return_value = query.all()
            logging.debug(f"return {return_value}")
            return return_value
        else:
            raise HTTPException(
                status_code=400,
                detail=f"No sites by user with id: {user_id}"
            )

    raise HTTPException(
        status_code=400,
        detail=f"No users with id: {id} exist."
    )

def get_sites_by_author_email(
        email: EmailStr,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if author_exists(db,email=email):
        author_id = get_author(db,data={"email":email},get="id")
        if author_id:
            return_value = db.query(models.Site).filter(models.Site.user_id == author_id).all()  # noqa: E501
            logging.debug(f"return {return_value}")
            return return_value

    raise HTTPException(
        status_code=400,
        detail="no records"
    )
        