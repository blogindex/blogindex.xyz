import logging
from sqlalchemy.orm import Session
import sys

from api import models

def author_exists(
        db: Session,
        email: str = "",
        id: int = 0,
        all_records: bool = False,
        is_scalar: bool = True
    ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")

    if all_records:
        query = db.query(db.query(models.Author).filter(models.Author.id > 0).exists)
        is_scalar = False
    elif id > 0:
        query = db.query(db.query(models.Author).filter(models.Author.id == id).exists())
        exists = query.scalar() if is_scalar else query.first()
    elif email != "":
        query = db.query(db.query(models.Author).filter(models.Author.email == email).exists())
        exists = query.scalar() if is_scalar else query.first()

    if exists and id > 0:
        author = db.query(models.Author).filter(models.Author.id == id).first()
        return author
    elif exists and email != "":
        author = db.query(models.Author).filter(models.Author.email == email).first()
        return author

    return False


def site_exists(
            db: Session,
            url: str = "",
            id: int = 0,
            user_id: int = 0,
            json: bool = False,
            all_records: bool = False,
            is_scalar: bool = True
            ):
    logging.debug(f"{sys._getframe().f_code.co_name}:\n{locals()}")
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
    logging.debug(f"{sys._getframe().f_code.co_name} RETURNS {query}:{return_value}")
    return [{query:return_value}] if json else return_value