from typing import Any, Generic, TypeVar, Type, List
from uuid import UUID

from fastapi.encoders import jsonable_encoder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import exc
from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, select

from db.models import User
from schema.user_schema import IUserCreate
from fastapi import status, HTTPException

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):
    def __init__(self, model: Type[ModelType], db_session: AsyncSession | None = None):
        
        self.model = model
        self.db_session = db_session
        
    async def create(
        self,
        obj_data: ModelType | CreateSchemaType
    ) -> ModelType:
        
        try:
            self.db_session.add(obj_data)
            await self.db_session.commit()
        except exc.IntegrityError:
            await self.db_session.rollback()
            raise HTTPException(status_code=409 , detail="Resuorce already exsists")
        self.db_session.refresh(obj_data)
        return obj_data

    async def get_by_id(
        self,
        model_id: int 
    ) -> ModelType:
        query = select(self.model).where(self.model.id == int(model_id))
        response = await self.db_session.execute(query)
        return response.scalar_one_or_none()
    
    async def get_all(self, limit: int= 10) -> List[ModelType]:  
        query = select(self.model).limit(limit)
        response = await self.db_session.exec(query)
        return [res for res in response]
    
    async def remove(self, *, id: UUID | str ) -> ModelType:
        response = await self.db_session.execute(
            select(self.model).where(self.model.id == id)
        )
        obj = response.scalar_one()
        await self.db_session.delete(obj)
        await self.db_session.commit()
        return obj

    async def update(
        self,
        *,
        obj_current: ModelType,
        data_in: UpdateSchemaType | dict[str, Any] | ModelType,
    ) -> ModelType:
        
        update_data = data_in.model_dump()
        for field in update_data:
            if update_data[field] is not None:
                setattr(obj_current, field, update_data[field])

        self.db_session.add(obj_current)
        await self.db_session.commit()
        await self.db_session.refresh(obj_current)
        return obj_current