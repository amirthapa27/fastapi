from typing import Optional
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime


# handles the data snet by the user to us

# defining a basemodel so that we can get the inputs of fieldtypes we define
class PostBase(BaseModel):
    title: str  # defining the field type
    content: str
    # setting default to true so if no value is given default value will be printed
    published: bool = True
    # rating: Optional[int] = None  # making it optional and default as none


class PostCretae(PostBase):  # inherit all the fields from PostBase
    pass


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:  # will tell the pydantic model to read the data even if its not a dict
        orm_mode = True

# handles us sending data to the user


class PostResponse(PostBase):
    # title: str
    # content: str
    # published: bool
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:  # will tell the pydantic model to read the data even if its not a dict
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    votes: int


# schema for creating user
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: int
