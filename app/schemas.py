from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from  pydantic.types import conint

class Post(BaseModel):
    title:str 
    content:str
    #published: bool = True
    # rating: Optional[int] = None 


class Postr(BaseModel):
    title:str
    content:str
    id:int
    created_at:datetime

    class Config:
        orm_mode = True 

class UserDetail(BaseModel):
    email:EmailStr
    password:str
   
class UserResponse(BaseModel):
    email:EmailStr
    id:int
    created_at:datetime

    #class Config:
        #orm_mode = True
        
class UserLogin(BaseModel):
    username:EmailStr
    password:str

class Token(BaseModel):
    acess_token:str
    token_type:str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir : conint(le=1)

