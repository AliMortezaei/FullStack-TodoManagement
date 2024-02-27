from typing import Generic, TypeVar, Type
from uuid import UUID

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, select


from schema.user_schema import IUserCreate, UserShow
from db.models import User
from db.models import Role


ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

class UserRepository():

    def __init__(self, db_session: AsyncSession) -> None:
        
        self.db_session = db_session


        
    async def get_by_username(self, username: str) -> User | None:
            
        query = select(User).where(User.username == username)
        response = await self.db_session.execute(query)
        return response.scalar_one_or_none()
        
    async def get_by_email(self, email: EmailStr) -> User | None:

        query = select(User).where(User.email == email)
        response = await self.db_session.execute(query)
        return response.scalar_one_or_none()

    async def get_user_and_email(
        self, user: ModelType | CreateSchemaType) -> tuple:
        username, email = ( await self.get_by_username(user.username),
                            await self.get_by_email(user.email)
                            )           
        return username , email 

    async def data_validate(self, data_in: IUserCreate) -> None:
        username, email = await self.get_user_and_email(data_in)

        if (username is not None) or (email is not None):
             raise HTTPException(status_code=409, detail="User already exsust with user name")
        return None

    async def all_user(self, limit) -> list:
        query = select(
            User.username,
            User.email,
            User.phone,
            User.first_name,
            User.last_name,
            User.brithdate
        ).limit(limit)
        response = await self.db_session.execute(query)
        return  [res for res in response]
            
