from uuid import UUID
from enum import Enum
from datetime import datetime
from typing import Optional, List

from pydantic import EmailStr
from sqlalchemy import BINARY
from sqlmodel import SQLModel, Field, Column, DateTime, Relationship, Enum, String

from .base_model import BaseUUIDModel
from .item_model import Item
from .role_model import Role


class UserBase(SQLModel):

    username: str = Field(unique=True, index=True)
    first_name: str = Field(nullable=True,default=None)
    last_name: str = Field(nullable=True, default=None)
    email: EmailStr = Field(sa_column=Column(String, index=True, unique=True))
    phone: str = Field(max_length=11, nullable=True)
    brithdate: Optional[datetime] = Field(nullable=True,default=None)
    

class User(BaseUUIDModel, UserBase, table= True):
    image: bytes = Field(BINARY, nullable=True)
    role_id: int = Field(foreign_key="role.id", default= 0)
    is_active: bool = Field(default=False)
    password: str | None = Field(
        default=False, nullable=False, index=True
    )
    role: Optional["Role"] = Relationship(
        back_populates="users", sa_relationship_kwargs={"lazy" : "joined"}
    )
    items : list['Item'] = Relationship(
        back_populates="user", sa_relationship={"lazy" : "selection"}
    )






