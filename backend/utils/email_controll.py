import smtplib, ssl
from datetime import timedelta
from typing import Callable
from abc import ABC, abstractmethod
from email.message import EmailMessage
from secrets import token_urlsafe

from fastapi import Depends, HTTPException, status
from pydantic import EmailStr

from schema.token_schema import TokenType
from core.redis import RedisManager, get_redis_db
from api import celery_task
from core.security import Expires, CreateEmailToken, TokenFactory
from core.config import settings
from utils.context_manager import SendEmailManager




class EmailLinkHandler:

    def __init__(self):
        self.redis_db: RedisManager = get_redis_db()

    @classmethod
    async def serializer(cls, user_id: int):
        token = CreateEmailToken(str(user_id)).make()
        restult = await cls().redis_db.add_token_to_redis(
            user_id, token,
            TokenType.EMAIL_TOKEN.value,
            timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES)
        )
        return token

    @classmethod
    async def desrializer(cls, token):
        pyload = TokenFactory()._decode(token)
        user_id = pyload["sub"]
        token = await cls().redis_db.get_token_redis(user_id, TokenType.EMAIL_TOKEN.value)
        if (not user_id) or token is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='invalid user')
        return user_id

    
# TODO: message must import html template created
class Messages:
    sender = settings.SENDER
    url = settings.API_V1_STR
    def __init__(self, link: str) -> None:
        self.link = f"http://{settings.ALLOWED_HOSTS}{self.url}/auth/verify/{link}"   
            
    def register(self):
         
        message = f"""
                    {self.sender} 
                    subject:
                            <b>This is HTML message.</b>
                            <h1>This is headline.</h1>
                            <h5>link: {self.link} </h5>
                    """
        return message
    

class EmailABC(ABC):
    Host = settings.HOST
    Port = settings.PORT
    UserName = settings.USERNAME
    Password = settings.PASSWORD
    Sender = settings.SENDER
    
    def __init__(
        self, user_id: int, email: EmailStr, ex: int | None = None
        ) -> None:
        
        self.user_id = user_id
        self.email = email
        self.ex = ex

    def send_email(
        self, 
        message: Callable[['Messages'], str] = None
        ):
        print(message)
        celery_task.send_email_task.delay(
            host=self.Host, port=self.Port,
            username = self.UserName, password=self.Password,
            sender=self.Sender, recever=self.email, message= message
            )
        
        return True

    @staticmethod
    def create_link(self): 
        pass

    @staticmethod
    def send(self, message):
        pass
    
class EmailVerify(EmailABC):

   
    async def generate_link(self):
        link = await EmailLinkHandler.serializer(str(self.user_id))
        return link

    async def send(self):
        link = await self.generate_link()
        return self.send_email(Messages(link).register())

    @classmethod
    async def verify(cls, token: str):
        user_id = await EmailLinkHandler.desrializer(token)
        return user_id
        