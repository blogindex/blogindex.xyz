from sqlalchemy import Boolean, ForeignKey, Integer, String, Float, Column, Boolean
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

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256), index=True)
    url = Column(String(256))
    description = Column(String(2048))
    moderation = Column(Boolean)
    disabled = Column(Boolean)
    rating = Column(Integer)
    user_id = Column(Integer)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(256))
    url = Column(String(256))
    excerpt = Column(String(1024))
    moderation = Column(Boolean)
    disabled = Column(Boolean)
    rating = Column(Integer)
    site_id = Column(Integer)

class Value(Base):
    __tablename__ = "value"

    id = Column(Integer, primary_key=True, index=True)
    post_id = Column(Integer)


class Split(Base):
    __tablename__ = "splits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128))
    method = Column(String(256))
    amount = Column(Integer)
    value_id = Column(Integer)
