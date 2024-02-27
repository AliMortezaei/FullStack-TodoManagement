from enum import Enum

from pydantic import BaseModel

from db.models import User

class TokenType(Enum):
    ACCESS_TOKEN = "access_token"
    REFRESH_TOKEN = "refresh_token"
    EMAIL_TOKEN = "email_token"

class CreateToken(BaseModel):
    token_type: TokenType
    user: User
    
class Token(BaseModel):
    access_token: str | None
    refresh_token: str
    token_type: str

class RefreshToken(BaseModel):
    token: str 

class AccessTokenOut(BaseModel):
    token: str
    token_type: TokenType

    