from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from . import models, schemas
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import ResponseValidationError
import random, string

def get_user_by_id(
            user_id: int,
            db: Session
            ):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            return user
        return []
    except:
        return []

def get_user_by_email(
            email: str,
            db: Session
            ):
    try:
        user = db.query(models.User).filter(models.User.email == email).first()
        print(user)
        if user:
            return user
        return []
    except ResponseValidationError:
        return []
    

def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(
            db: Session,
            user: schemas.UserCreate
            ):
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

    user = db.query(models.User).filter(models.User.id == key.user_id).first()
    if user:
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
    user_keys = db.query(models.Key).filter(models.Key.user_id == user_id).all()
    if user_keys:
        return [user_keys]
    raise HTTPException(
            status_code=400,
            detail = f"User with user_id {user_id} has no keys."
            )
