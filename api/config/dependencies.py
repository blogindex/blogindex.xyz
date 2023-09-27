
import sys
from os import environ

from fastapi.security import HTTPBearer

from .configure import Configure
from .database import database
from api import models

if "BLOGINDEX_DEBUG" not in environ or environ["BLOGINDEX_DEBUG"] != "True":
    sys.tracebacklimit = 0

Config = Configure()
config = Config.get()
dbase = database(config)

# HTTP Bearer Authentication
token_auth_scheme = HTTPBearer()

models.Base.metadata.create_all(bind=dbase.engine)

def get_db():
    db = dbase.SessionLocal()
    try:
        yield db
    finally:
        db.close()