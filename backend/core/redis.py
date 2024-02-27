from datetime import timedelta
from uuid import UUID
from typing import Any

from fastapi import HTTPException
from redis.asyncio import ConnectionPool, Redis

from schema.token_schema import TokenType
from .config import settings


pool = ConnectionPool.from_url(url= settings.REDIS_URL,max_connections=100)

class RedisManager:

    def __init__(self):
        self.redis = Redis(connection_pool=pool)

    def serializer(self, user_id: str, token_type: TokenType):
        return f'{user_id}:{token_type}'

    def desrializer(self):
        pass


        
    async def add_token_to_redis(
        self,
        user_id: UUID | str,
        token: str,
        token_type: TokenType,
        expire_time: int
    ) -> bool:
        try:
            key = self.serializer(str(user_id), token_type)
            await self.redis.set(key, token, ex=expire_time)
        except Exception as exp:
            raise HTTPException(status_code=500, detail="connection failed")
        return True
    
    async def get_token_redis(
        self,
        user_id: UUID | str,
        token_type: TokenType, 
    ) -> str:
        try:
            key = self.serializer(str(user_id), token_type)
            token = await self.redis.get(key)
        except Exception as exp:
            raise HTTPException(status_code=403, detail='token timeout , login ')
        return token

def get_redis_db():
    return RedisManager()
        

        
            