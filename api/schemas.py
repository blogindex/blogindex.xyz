from pydantic import ConfigDict, BaseModel, EmailStr, conint, conlist, Json, constr, HttpUrl
from typing import Optional, Any, Union

# model.Author
class AuthorBase(BaseModel):
    email: EmailStr
    first_name: constr(max_length=32) = ""
    last_name: constr(max_length=32) = ""
    display: constr(min_length=4,max_length=32)
    image: constr(min_length=12,max_length=2083) = "https://theblogindex.org/img/no-image.svg"
    avatar: constr(min_length=12,max_length=2083) = "https://theblogindex.org/img/no-image.svg"
    flags: list[constr(max_length=32)] = []
    rating: conint(ge=1,lt=101) = 100
    disabled: bool = False
    value: list[constr(max_length=256)] = []

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

# model.Site
class SiteBase(BaseModel):
    url: constr(min_length=12,max_length=2083)
    name: constr(min_length=5,max_length=500)
    description: constr(max_length=2048)
    rating: conint(ge=1,lt=101) = 100
    flags: list[constr(max_length=32)] = []
    disabled: bool = False
    value: list[constr(max_length=256)] = []

class SiteCreate(SiteBase):
    user_id: int

class Site(SiteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int

# model.Post
class PostBase(BaseModel):
    url: constr(min_length=12,max_length=2083)
    name: constr(min_length=5,max_length=500)
    excerpt: constr(max_length=2048)
    rating: conint(ge=1,lt=101) = 100
    flags: list[constr(max_length=32)] = []
    disabled: bool = False
    value: list[constr(max_length=256)] = []

class PostCreate(PostBase):
    user_id: int
    site_id: int

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    site_id: int

