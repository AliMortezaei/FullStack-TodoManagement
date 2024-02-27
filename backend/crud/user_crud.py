from typing import List
from datetime import timedelta
from uuid import uuid4, UUID
from typing import Annotated

from jose import jwe, ExpiredSignatureError
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from pydantic import Field

from core.config import settings
from core.redis import RedisManager, get_redis_db
from schema.user_schema import RoleEnum
from db.models import User
from crud.crud_base import CRUDBase, ModelType
from schema.user_schema import IUserCreate, UserOutRegister, UserLogin,UserShow
from schema.token_schema import TokenType, AccessTokenOut
from core.exceptions import BadRequestException
from core.security import PasswordHandler, CreateAccessToken
from core.config import settings
from utils.email_controll import EmailVerify
from db.repository import UserRepository 


class CRUDUser(CRUDBase[User, IUserCreate]):
    password_handler = PasswordHandler

    def __init__(self, db_session):
        super().__init__(User , db_session)
        self.adapter = UserRepository(db_session)


    async def registration(self, data_in: IUserCreate) -> UserOutRegister:
        await self.adapter.data_validate(data_in)
        
        hashed_password = self.password_handler.get_password_hash(password=data_in.password)
        user = await self.create_user(data_in, hashed_password)
        if user is not None:
           await EmailVerify(user_id= user.id, email= user.email).send()
            
        return user

    async def create_user(self, data_in: IUserCreate, hashed_password: str) -> UserOutRegister:
        delattr(data_in, "confirm_password")
        data_in.password = hashed_password
        data_in.image = settings.DEFULT_IMAGE
        obj_data = User.model_validate(data_in)
        result = await self.create(obj_data)
        return obj_data


    async def verify(self, user_id: int) -> User:
        user = await self.get_by_id(user_id)        
        if user.is_active == True:
            raise HTTPException(
                status_code=302,
                detail="The user is active. Please be redirected to the login page to continue."
            )
        user.is_active = True
        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)   
        return user

    async def authentication(self, data_in: UserLogin) -> User:
        user = await self.adapter.get_by_email(data_in.email)
        if (not user) or (not self.password_handler.verify_password(
                data_in.password, user.password
        )):
            raise HTTPException(status_code=400, detail="email or password incorrect")
        elif user.is_active != True:
            raise HTTPException(status_code=400, detail="User is inactive")
        
        return user


    async def get_all_user(self, limit: int=10) :
        users = await self.adapter.all_user(limit)
        return [UserShow(
            username= user[0],
            email= user[1],
            phone= user[2],
            first_name= user[3],
            last_name= user[4],
            brithdate= user[5]
        ) for user in users]
        

    async def refresh_valied(
        self,
        user_id: str,
        refresh: str ,
        redis_client: RedisManager
    ):   

        valied_token = await redis_client.get_token_redis(
            user_id= user_id, token_type=TokenType.REFRESH_TOKEN.value
        )
        if refresh not in str(valied_token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail="Refresh token invalid")
        user = await self.get_by_id(user_id)
        if user.is_active == False:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "User in Inactive")

        access_token = CreateAccessToken(user_id).make()
        await redis_client.add_token_to_redis(
            user_id= str(user.id),
            token= access_token,
            token_type= TokenType.ACCESS_TOKEN.value,
            expire_time= timedelta(minutes= settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return AccessTokenOut(token= access_token, token_type= TokenType.ACCESS_TOKEN.value)


        







        