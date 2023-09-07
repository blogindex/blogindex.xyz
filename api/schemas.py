from pydantic import ConfigDict, BaseModel, EmailStr, conint, conlist, Json, constr, HttpUrl
from typing import Optional, Any

# model.Key
class KeyBase(BaseModel):
    permissions: conlist(str) = []

class KeyCreate(KeyBase):
    user_id: conint(ge=1)

class KeyUpdate(KeyBase):
    permissions: conlist(str) = []

class KeyDisplay(KeyBase):
    user_id: int
    key: str

class Key(KeyBase):
    user_id: conint(ge=1)
    permissions: Json[list[constr(max_length=10)]]

class KeyList(BaseModel):
    key:str

# model.User
class UserBase(BaseModel):
    email: EmailStr
    display: str
    moderation: Optional[bool] = False
    rating: Optional[conint(ge=1,lt=101)] = 100
    disabled: Optional[bool] = False

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    hashed_password: str = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# model.Site
class SiteBase(BaseModel):
    url: constr(min_length=12,max_length=2083)
    name: constr(min_length=5,max_length=500)
    description: constr(max_length=2048)
    moderation: Optional[bool] = False
    rating: Optional[conint(ge=1,lt=101)] = 100
    disabled: Optional[bool] = False
    value: list[constr(max_length=128)] = []

class SiteCreate(SiteBase):
    user_id: int

class Site(SiteBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int

# model.Page
class PageBase(BaseModel):
    url: constr(min_length=12,max_length=2083)
    name: constr(min_length=5,max_length=500)
    excerpt: constr(max_length=2048)
    moderation: Optional[bool] = False
    rating: Optional[conint(ge=1,lt=101)] = 100
    disabled: Optional[bool] = False
    value: list[constr(max_length=128)] = []

class PageCreate(PageBase):
    user_id: int
    site_id: int

class Page(PageBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    site_id: int

