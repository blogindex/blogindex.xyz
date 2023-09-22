from sqlalchemy import Boolean, ForeignKey, Integer, String, Float, Column, Boolean, ARRAY, Unicode, LargeBinary
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship, DeclarativeBase
from pprint import pprint

print(__name__)

class Base(DeclarativeBase):
    pass

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    display = Column(Unicode(32))
    image = Column(String(2048))
    avatar = Column(String(2048))
    flags = Column(ARRAY(String(32)))
    rating = Column(Integer)
    disabled = Column(Boolean)
    value = Column(ARRAY(String(256)))

class Site(Base):
    __tablename__ = "sites"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    url = Column(Unicode(2083))
    name = Column(Unicode(500))
    description = Column(Unicode(2048))
    rating = Column(Integer)
    flags = Column(ARRAY(String(32)))
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
    flags = Column(ARRAY(String(32)))
    disabled = Column(Boolean)
    value = Column(ARRAY(String(256)))

