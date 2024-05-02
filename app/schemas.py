from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Annotated, Optional, Text
from dataclasses import dataclass


#Base models:

#Login
class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None



#Users:
class User(BaseModel):
    username: str


class UserOut(User):
    email: EmailStr
    id : int
    created_at: datetime
    

class CreateUser(User):
    email: EmailStr
    password: str
    created_at: datetime = datetime.now()

class EditUser(User):
    email: EmailStr
    password: str



#Post:
class PostBase(BaseModel):
    title: str
    content: Text
    published: bool = False


class CreatePost(PostBase):
    id: Optional[int] = None
    created_at: datetime = datetime.now()

    
class Post(PostBase):
    id: int
    created_at: datetime = datetime.now()
    owner_id: int
    owner: User

    #class Config:
    #    orm_mode= True


class PostOut(BaseModel):
    Post: Post
    likes: int


class UpdatedPost(PostBase):
    edited: bool = True
    edited_at: datetime = datetime.now()



#Votes:
@dataclass
class ValueRange:
    lo: int
    hi: int


class Vote(BaseModel):
    post_id: int
    #dir: Annotated[int, ValueRange(0, 1)]
    dir: bool = False