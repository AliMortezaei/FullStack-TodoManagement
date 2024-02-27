
from datetime import datetime, timedelta

from passlib.context import CryptContext
from jose import jwt

from schema.token_schema import TokenType
from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




class Expires:
    @staticmethod
    def access_time():
        return datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    @staticmethod
    def refresh_time():
        return datetime.now() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    @staticmethod
    def email_token():
        return datetime.now() + timedelta(minutes=settings.EMAIL_TOKEN_EXPIRE_MINUTES) 

class TokenFactory:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM


    def make(self):
        pyload ={
            "type": self.token_type,
            "sub": str(self.sub),
            "exp": self.exp
        }
        return jwt.encode(pyload, key=self.secret_key, algorithm=self.algorithm)

        
    def _decode(self, token: str) -> str:
        return jwt.decode(token, key=self.secret_key, algorithms=self.algorithm)
        
    

class CreateAccessToken(TokenFactory):
    def __init__(self, sub, exp: datetime = Expires.access_time()):
        super().__init__()
        self.sub = sub
        self.exp = exp
        self.token_type = TokenType.ACCESS_TOKEN.value

            
class CreateRefreshToken(TokenFactory):

    def __init__(self, sub, exp: datetime = Expires.refresh_time()):
        super().__init__()
        self.sub = sub
        self.exp = exp
        self.token_type = TokenType.REFRESH_TOKEN.value
            

class CreateEmailToken(TokenFactory):
    def __init__(self, sub, exp: datetime = Expires.email_token()):
        super().__init__()
        self.sub = sub
        self.exp = exp
        self.token_type = TokenType.EMAIL_TOKEN.value



    
class PasswordHandler:

    @staticmethod
    def get_password_hash(password: str):
        return pwd_context.hash(password)

    def verify_password(plain_password, hashed_password) -> bool:
        return pwd_context.verify(plain_password, hashed_password)