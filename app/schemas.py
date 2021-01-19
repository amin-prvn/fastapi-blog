from typing import List, Optional

from pydantic import BaseModel, validator, ValidationError


class PostBase(BaseModel):
    title: str
    contents: str = None
    


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    photo: str
    owner_id: int

    class Config:
        orm_mode = True

########## User Schemas ##########

class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    phone: str
    password: str
    confirmed_password: str

    @validator('confirmed_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match!')
        return v


class UserLogin(UserBase):
    password: str
    

class User(UserBase):
    name: str
    id: int
    posts: List[Post] = []

    class Config:
        orm_mode = True




