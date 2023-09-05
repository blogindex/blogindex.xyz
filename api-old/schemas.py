from pydantic import BaseModel, Field, constr, conint

# Pydantic model for User
class UserBase(BaseModel):
    email: constr(max_length=100)
    display: constr(max_length=20)

class UserCreate(UserBase):
    hashed_password: str
    moderation: bool = False
    disabled: bool = False
    rating: conint(gt=0, lt=101) = 100

class User(UserBase):
    id: int
    moderation: bool = False
    disabled: bool = False
    rating: conint(gt=0, lt=101) = 100

    class Config:
        from_attributes = True

# Pydantic model for Site
class SiteBase(BaseModel):
    title: constr(max_length=256)
    url: constr(max_length=256)
    description: constr(max_length=2048)
    userid: int

class SiteCreate(SiteBase):
    moderation: bool = False
    disabled: bool = False
    rating: conint(gt=0, lt=101) = 100

class Site(SiteBase):
    id: int
    moderation: float = 0.0

    class Config:
        from_attributes = True


# Pydantic model for Post
class PostBase(BaseModel):
    title: constr(max_length=256)
    url: constr(max_length=256)
    excerpt: constr(max_length=2048)
    site_id: int

class PostCreate(PostBase):
    moderation: bool = False
    disabled: bool = False
    rating: conint(gt=0, lt=101) = 100

class Post(PostBase):
    id: int

    class Config:
        from_attributes = True



# Pydantic model for Value
class ValueBase(BaseModel):
    post_id: int

class ValueCreate(ValueBase):
    pass

class Value(ValueBase):
    id: int

    class Config:
        from_attributes = True

# Pydantic model for Split
class SplitBase(BaseModel):
    name: str
    method: str
    amount: int
    value_id: int

class SplitCreate(SplitBase):
    pass

class Split(SplitBase):
    id: int

    class Config:
        from_attributes = True