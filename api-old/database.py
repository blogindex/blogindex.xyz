from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLITE
# SQLALCHEMY_DATABASE_URL = "sqlite:///./api.db"

# MariaDB
SQLALCHEMY_DATABASE_URL = "mariadb+mariadbconnector://blogindex:blogindex@mariadb:3306/blogindex"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
    #,connect_args={"check_same_thread": False}  # <-- This is for SQLITE ONLY
    )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
