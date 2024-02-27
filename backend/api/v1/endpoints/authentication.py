from typing import Annotated
from uuid import UUID
from datetime import timedelta

from jose import jwt, ExpiredSignatureError
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import APIRouter, Depends, Request, Body, status, HTTPException
from sqlalchemy import exc

from core.config import settings
from core.security import Expires, CreateAccessToken, CreateRefreshToken, TokenFactory
from db.models import User
from api.deps import get_db
from utils.email_controll import EmailVerify
from schema.token_schema import TokenType, Token, RefreshToken, AccessTokenOut
from schema.user_schema import IUserCreate, UserOutRegister, UserLogin
from core.redis import RedisManager, get_redis_db
from crud import CRUDUser


router = APIRouter()

@router.post("/register")
async def register(
    data_in: IUserCreate,
    db_session: AsyncSession = Depends(get_db)
) -> UserOutRegister:
      
    return await CRUDUser(db_session).registration(data_in)
        
        
@router.get("/verify/{token}")
async def verify(
    user_id: int = Depends(EmailVerify.verify),
    db_session: AsyncSession = Depends(get_db)
) -> UserOutRegister:

    return await CRUDUser(db_session).verify(user_id)

@router.post("/login", response_model=Token)
async def login(
    data_in: UserLogin,
    db_session: AsyncSession = Depends(get_db),
    redis_client: RedisManager = Depends(get_redis_db),
) -> Token:
    user = await CRUDUser(db_session).authentication(data_in)
    
    access_token = CreateAccessToken(user.id).make()
    refresh_token = CreateRefreshToken(user.id).make()
    data = Token(
        access_token= access_token,
        refresh_token= refresh_token,
        token_type="Bearer"
    )
    await redis_client.add_token_to_redis(
        user_id=user.id,
        token=access_token,
        token_type=TokenType.ACCESS_TOKEN.value,
        expire_time= timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    await redis_client.add_token_to_redis(
        user_id=user.id,
        token=refresh_token,
        token_type=TokenType.REFRESH_TOKEN.value,
        expire_time= timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )
    return data

@router.post("/new_access_token")
async def get_new_access_token(
    refresh: RefreshToken = Body(...),
    db_session: AsyncSession = Depends(get_db),
    redis_client: RedisManager = Depends(get_redis_db)
) -> AccessTokenOut:

    try:
        pyload = TokenFactory()._decode(refresh.token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your token has expired. Please log in again.",
        )
         
    if pyload["type"] != TokenType.REFRESH_TOKEN.value:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail="Incorrect Token"   
        )
    user_id = pyload["sub"]
    
    return await CRUDUser(db_session).refresh_valied(user_id, refresh.token, redis_client)
               
 




