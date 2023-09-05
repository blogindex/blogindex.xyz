from pydantic import BaseModel, EmailStr, conint, conlist
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr
    display: str
    moderation: Optional[bool] = False
    rating: Optional[conint(ge=1)] = 100
    disabled: Optional[bool] = True

class UserCreate(UserBase):
    hashed_password: str

class UserUpdate(UserBase):
    hashed_password: str = None

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


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
    permissions: conlist(str) = []

class KeyList(BaseModel):
    key:str
