import logging
from sqlalchemy.orm import Session

from api import models

def user_exists(
        db: Session,
        email: str = "",
        id: int = 0,
        all_records: bool = False,
        is_scalar: bool = True
    ):
    logging.debug(f"Function call:\n\
        user_exists(\n\
            db: Session = {db},\n\
            email: str = {email}\n\
            id: int = {int}\n\
            all_records: bool = {all},\n\
            is_scalar: bool = {is_scalar}\n\
        ):"
    )
    if all_records:
        query = db.query(db.query(models.User).filter(models.User.id > 0).exists)
        is_scalar = False
    elif id > 0:
        query = db.query(db.query(models.User).filter(models.User.id == id).exists())
    elif email != "":
        query = db.query(db.query(models.User).filter(models.User.email == email).exists())
    return_value = query.scalar() if is_scalar else query.first()
    return return_value


def site_exists(
            db: Session,
            url: str = "",
            id: int = 0,
            user_id: int = 0,
            json: bool = False,
            all_records: bool = False,
            is_scalar: bool = True
            ):
    logging.debug(f"\n\
    site_exists(\n\
        db: Session = {db},\n\
        url: int = {url},\n\
        id: int = {id},\n\
        user_id: int = {user_id},\n\
        json: bool = {bool},\n\
        all_records: bool = {all_records},\n\
        is_scalar: bool = {is_scalar},\n\
        ):")
    if all_records:
        query = db.query(db.query(models.Site).exists())
    elif id > 0:
        query = db.query(db.query(models.Site).filter(models.Site.id == id).exists())
    elif user_id > 0:
        query = db.query(db.query(models.Site).filter(models.Site.user_id == user_id).exists())
    else:
        query = db.query(db.query(models.Site).filter(models.Site.url == url).exists())
    if is_scalar:
        return_value = query.scalar() if is_scalar else query.fist()
    logging.debug(f"site_exists() RETURNS {query}:{return_value}")
    return [{query:return_value}] if json else return_value