from typing import List
from enum import Enum, auto
from fastapi import HTTPException
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator


class RoleEnum(Enum):
    User = auto()
    Consultant = auto()    
    

class UserBase(BaseModel):

    username: str 
    email: EmailStr 
    phone: str = Field(max_length=11)


class IUserCreate(UserBase):
    
    password: str  
    confirm_password: str

    # TODO: field password validator 8 min lenght 
    @model_validator(mode='after')
    def verifypassword(self):
        if self.password != self.confirm_password:
            raise HTTPException(
                status_code=401,
                detail="moust confirm passwrod equel password "
            )
        return self 
    

class UserLogin(BaseModel):
    email: EmailStr
    password: str

    
class UserOutRegister(UserBase):
    pass

class UserShow(UserBase):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    brithdate: datetime | None = None
    image: str | None = Field(default=None)

class UserProfileUpdate(BaseModel):

    first_name: str | None = None
    last_name: str | None = None
    brithdate: datetime | None = None
    image: str | None = Field(default=None)
