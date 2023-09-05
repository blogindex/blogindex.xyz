from sqlalchemy import Boolean, ForeignKey, Integer, String, Float, Column, Boolean, ARRAY
from sqlalchemy.orm import relationship, DeclarativeBase

from .database import Base

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(256))
    display = Column(String(20))
    moderation = Column(Boolean)
    rating = Column(Integer)
    disabled = Column(Boolean)

class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    key = Column(String(255))
    permissions = Column(ARRAY(String))