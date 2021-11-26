
from re import S
from pydantic import BaseModel


from pydantic.networks import EmailStr
from pydantic.types import conint

from datetime import datetime
from typing import Optional

from app.database import Base          # Wow, this is interesting, this got imported automatically!

class UserBase(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class UserCreate(UserBase):                # We don't expect anything else
    pass

class User(BaseModel):                      # Why would we send back password ever?! Clang...
    id: int
    email: EmailStr
    created_at: datetime                    # why was this missing?

    class Config:
        orm_mode = True

class UserLogin(BaseModel):                 # To be used in authentication  -- In Improvements, this is overridden
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


class PostBase(BaseModel):                      # remember this is from Pydantic
    #id: int
    title: str
    content: str
    published: bool = True                  # Optional parameter but default value
    #rating: Optional[int] = None            # Check the difference: We are telling this to be optional
                                            # if present, it needs to be int, but if not present, it is None (null)
    def __getitem__(self, item):            # This is some magic I had to add if I want the list to contain Posts, and not dicts of Posts
        return getattr(self, item)

class PostCreate(PostBase):                     # Why did he do this? Not entirely clear right now.
    pass


class Post(PostBase):                      # this is a pydantic model, remember, to be used for Responses
    id: int
    created_at: datetime
    owner_id: int                           # This is a new addition. But this is going to be picked up from the authentication info
    owner: User

    class Config:                           # Normally Pydantic works with dict. But responses are sqlalchemy models..
        orm_mode = True                     # So this class tells Pydantic to treat it as such...



class PostOnly(PostBase):
    id: int
    created_at: datetime
    owner_id: int

    class Config:                           # Normally Pydantic works with dict. But responses are sqlalchemy models..
        orm_mode = True                     # So this class tells Pydantic to treat it as such...


class PostOut(BaseModel):                        # Added as we were trying to get the votes for the post
    Post: PostOnly                     
                                            # Whats your problem? If I leave this in here and do not inherit, fastapi.exceptions.FastAPIError: Invalid args for response field! Hint: check that typing.List[app.schemas.PostOut] is a valid pydantic field type
                                            # ^^ The problem above was, I had forgotten to inherit BaseModel... So it could not understand the pydantic relationship...
    votes: int

    class Config:                           # Normally Pydantic works with dict. But responses are sqlalchemy models..
        orm_mode = True                     # So this class tells Pydantic to treat it as such...


class Token(BaseModel):                     # This is when we return the token and its type to the client
    access_token: str
    token_type: str
    # token_expiry: str                     # ideally, I will like to add this. But I am not able to figure out the oauth2_scheme at present.


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)                       # This is something from pydantic, will allow less than or equal to 1

    class Config:
        orm_mode = True
