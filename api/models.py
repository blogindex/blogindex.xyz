from sqlalchemy import Boolean, ForeignKey, Integer, String, Float, Column, Boolean, ARRAY, Unicode
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, DeclarativeBase

from .database import Base

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(256))
    display = Column(Unicode(20))
    moderation = Column(Boolean)
    rating = Column(Integer)
    disabled = Column(Boolean)

class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    key = Column(String(255))
    permissions = Column(JSONB)

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    url = Column(Unicode(2083))
    name = Column(Unicode(500))
    description = Column(Unicode(2048))
    rating = Column(Integer)
    moderation = Column(Boolean)
    disabled = Column(Boolean)
    value = Column(ARRAY(String(256)))

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    site_id = Column(Integer)
    url = Column(Unicode(2083))
    name = Column(Unicode(1024))
    excerpt = Column(Unicode(2048))
    rating = Column(Integer)
    moderation = Column(Boolean)
    disabled = Column(Boolean)
    value = Column(ARRAY(String(256)))

