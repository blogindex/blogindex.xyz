import logging
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import EmailStr, ValidationError
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, ProgrammingError
import random, string

from . import models, schemas

def get_user_by_id(
            user_id: int,
            db: Session
            ):
    """ GET row of a single user defined by the `id`

    Args:
        user_id (int): user's `id`
        db (Session): Database Session

    Returns:
        _type_: _description_
    """
    logging.debug(f"Function call:\n\
                get_user_by_id(\n\
                    user_id: int = {user_id}\n\
                    db: Session = {db},\n\
                )"
                )
    if user_exists_by_id(user_id,db):
        user = db.query(models.User).filter(models.User.id == user_id).first()
        return user
    else:
        raise HTTPException(
                status_code=400,
                detail=f"No users with `id` == `{id}` exist."
                )

def get_user_by_email(
            email: str,
            db: Session
            ):
    logging.debug(f"Function call:\n\
                get_user_keys(\n\
                    email: str = {email}\n\
                    db: Session = {db},\n\
                )"
                )
    if user_exists_by_email(email,db):
        user = db.query(models.User).filter(models.User.email == email).first()
        return user
    else:
        raise HTTPException(
                status_code=400,
                detail=f"No users with `email` == {email} exist."
                )

def get_all_users(
            db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    logging.debug(f"Function call:\n\
                get_user_keys(\n\
                    db: Session = {db},\n\
                    skip: int = {skip}\n\
                    limit: int = {limit}\n\
                )"
                )
    query = db.query(models.User).offset(skip).limit(limit) 
    if db.query(query.exists()).first():
        return query.all()
    else:
        raise HTTPException(
                status_code=400,
                detail=f"No users exist.  That seems strange.¯\_(ツ)_/¯"
                )


def create_user(
            db: Session,
            user: schemas.UserCreate
            ):
    logging.debug(f"Function call:\n\
                get_user_keys(\n\
                    db: Session = {db},\n\
                    user: schemas.UserCreate = {user}\n\
                )"
                )
    """ Creates and inserts a new user into the database

    Args:
        db (Session): Database Connector
        user (schemas.UserCreate): Pydantic Model

    Returns:
        schemas.User: Pydantic Model
    """
    fake_hashed_password = user.hashed_password + "notreallyhashed"
    db_user = models.User(email=user.email, display=user.display, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_key(
            key: schemas.KeyDisplay,
            db: Session
            ):
    logging.debug(f"Function call:\n\
                get_user_keys(\n\
                    key: schemas.KeyDisplay = {key}\n\
                    db: Session = {db},\n\
                )"
                )
    """ Generates and inserts a new API Key into the database

    Args:
        key (schemas.KeyDisplay): Pydantic Schema
        db (Session): Database Connector

    Returns:
        schemas.KeyDisplay: Pydantic Model which redacts sensitive information
    """
    def generate_key():
        """Generates an API Key in the following format:
        32 alphanumeric  characters grouped in 4 characters separated by dashes.
        For example:
            `KKVy-0B6G-JzBz-NweS-p6sU-GhaX-hHYk-zIcM`

        Returns:
            str: API Key as shown above
        """
        return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

    if user_exists_by_id(key.user_id,db):
        key_in = generate_key()
        key_out = ""
        for i in range(0, len(key_in), 4):
            key_out += key_in[i:i+4] + "-"
        db_key = models.Key(
            user_id = key.user_id,
            key = key_out.rstrip("-"),
            permissions = key.permissions
        )
        db.add(db_key)
        db.commit()
        db.refresh(db_key)
        return [db_key]
    raise HTTPException(
            status_code=400,
            detail = f"User with user_Id {key.user_id} does not exist."
            )

def get_user_keys(
            user_id: int,
            db: Session
            ):
    logging.debug(f"Function call:\n\
                get_user_keys(\n\
                    user_id: int = {user_id}\n\
                    db: Session = {db},\n\
                )"
                )
            
    """Retrieves keys for a specific user

    Args:
        user_id (int): unique user id
        db (Session): Database Connector

    Raises:
        HTTPException: If user does not exist, raises HTTP 400

    Returns:
        schema.Key: Returns a list of user keys to authenticate with.
                    This should *NOT* be made available with an endpoint in production
                    Use WISELY!!!!!
    """
    user_keys = db.query(models.Key).filter(models.Key.user_id == user_id).all()
    if user_keys:
        return [user_keys]
    raise HTTPException(
            status_code=400,
            detail = f"User with user_id {user_id} has no keys."
            )

def create_site(
            db:Session,
            site: schemas.SiteCreate
            ):
    logging.debug(f"Function call:\n\
                create_site(\n\
                    db = {db},\n\
                    site = {site}\n\
                )"
                )
    try:
        user_id = db.query(models.User).filter(models.User.id == site.user_id).first()
    except ProgrammingError:
        raise HTTPException(
                status_code=400,
                detail=f"User with id: {site.user_id} does not exist.\
                    You must provide a valid user_id to attach this site to." 
                )
    
    try:
        url = db.query(models.Site).filter(models.Site.name == site.url).first().url
    except AttributeError:
        url = ""
    try:
        name = db.query(models.Site).filter(models.Site.name == site.name).first().name
    except AttributeError:
        name = ""

    if url:
        try:
            user = db.query(models.User).filter(models.User.id == url.user_id).first()
            display = user.display
            email = user.email
        except:
            display = "Unknown"
            email = "Unknown"
        raise HTTPException(
                status_code=400,
                detail=f"URL already exists and owned by {user.display}:{user.email}.\
                    Please contact support@blogindex.xyz if this is an error."
                )
    if name and url:
        user = db.query(models.User).filter(models.User.id == name.user_id).first()
        raise HTTPException(
                status_code=400,
                detail=f"Site named {site.name} exists with a url of {url} owned by\
                    {user.display}:{user.email}.  If you would like to duplicate this title,\
                    use `/site/create/dup_name` endpoint.  If you believe use of this name is\
                    a violation of your rights, please contact support@blogindex.xyz"
                )
    try:
        db_site = models.Site(
                url = site.url,
                name = site.name,
                description = site.description,
                moderation = False,
                rating = 100,
                disabled = False,
                value= site.value,
                user_id = site.user_id
                )

        db.add(db_site)
        db.commit()
        db.refresh(db_site)
    except ResponseValidationError as error:
        raise HTTPException(
                status_code=400,
                detail=f"Validation Error:{error}"
        )
    return [db_site]

def get_all_sites(
            db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    logging.debug(f"Function call:\n\
                get_all_sites(\n\
                    db: Session = {db},\n\
                    skip: int = {skip}\n\
                    limit: int = {limit}\n\
                )"
                )
    return db.query(models.Site).offset(skip).limit(limit).all()

def get_sites_by_site_id(
            site_id: int,
            db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    logging.debug(f"Function call:\n\
                get_sites_by_site_id(\n\
                    site_id: int = {site_id},\n\
                    db: Session = {db},\n\
                    skip: int = {skip},\n\
                    limit: int = {limit}\n\
                )"
                )
    site = db.query(models.Site).filter(models.Site.id == site_id).first()
    return site

def get_sites_by_user_id(
            user_id: int,
            db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    logging.debug(f"Function call:\n\
                get_sites_by_user_id(\n\
                    user_id: int = {user_id},\n\
                    db: Session = {db},\n\
                    skip: int = {skip},\n\
                    limit: int = {limit}\n\
                )"
                )
    if user_exists_by_id(user_id,db):
        return_value = db.query(models.Site).filter(models.Site.user_id == user_id).first()
        if return_value:
            return return_value
        else:
            raise HTTPException(
                status_code=400,
                detail=f"No sites by user with id: {user_id}"
            )
        logging.debug(f"\n\
        return {return_value}")
    else:
        raise HTTPException(
                status_code=400,
                detail=f"No users with id: {id} exist."
                )

def get_sites_by_user_email(
            email: EmailStr,
            db: Session,
            skip: int = 0,
            limit: int = 100
            ):
    logging.debug(f"Function call:\n\
                get_sites_by_user_email(\n\
                    email: int = {email},\n\
                    db: Session = {db},\n\
                    skip: int = {skip},\n\
                    limit: int = {limit}\n\
                ):"
                )

    if user_exists_by_email(email,db):
        return db.query(models.Site).filter(models.Site.user_id == user.id).all()
    else:
        raise HTTPException(
                status_code=400,
                detail=f"No users with email: {email} exist."
                )
        


def user_exists_by_email(
            email: str,
            db: Session
            ):
    exists = db.query(db.query(models.User).filter(models.User.email == email).exists()).scalar()
    logging.debug(f"\n\
    user_exists_by_email(\n\
        email: str = {email},\n\
        db: Session = {db}\n\
        ):\n\
    return {exists}")
    return exists

def user_exists_by_id(
            user_id: int,
            db: Session,
            json: bool = False
            ):
    logging.debug(f"\n\
    user_exists_by_id(\n\
        user_id: int = {id},\n\
        db: Session = {db}\n\
        ):")
    exists = db.query(db.query(models.User).filter(models.User.id == user_id).exists()).scalar()
    logging.debug(f"return {exists}")
    return exists

def exists_in_db(
            query,
            db,
            scalar: bool = False,
            json: bool = False
            ):
    exists = db.query(db.query(query.exists))
    exists = exsists.scalar() if scalar else exists.first()
    return [{query:exists}] if json\
                            else exists