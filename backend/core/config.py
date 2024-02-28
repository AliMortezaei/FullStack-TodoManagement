
import os, sys
from tokenize import Pointfloat
from typing import Any
from dotenv import load_dotenv

from pydantic import BaseModel, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))
sys.path.append(BASE_DIR)

class Settings(BaseSettings):
    PORT_HOST: int = os.environ["PORT_HOST"]
    API_V1_STR: str = "/api/v1"
    ALLOWED_HOSTS: str = os.environ["ALLOWED_HOSTS"]
    SECRET_KEY: str = "test@asfwdv333dscc1233"
    EMAIL_kEY: str = b'testkey'
    DEFULT_IMAGE: str = f"http://{ALLOWED_HOSTS}:{PORT_HOST}/media/IMG_20240221_193907_257.jpg"
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1  
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 100  # 100 days
    EMAIL_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3 # 3 days
    DB_POOL_SIZE: int = 83
    # email config
    HOST: str = os.environ["EMAIL_HOST"]
    PORT: int = os.environ["EMAIL_PORT"]
    USERNAME: str = os.environ["EMAIL_USERNAME"]
    PASSWORD: str = os.environ["EMAIL_PASSWORD"]
    SENDER: EmailStr = os.environ["EMAIL_SENDER"]
    # redis server
    REDIS_HOST: str = os.environ["REDIS_HOST"]
    REDIS_PORT: str = os.environ["REDIS_PORT"]
    REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"

    DATABASE_USER: str = os.environ["DATABASE_USER"]
    DATABASE_PASSWORD: str = os.environ["DATABASE_PASSWORD"]
    DATABASE_HOST: str = os.environ["DATABASE_HOST"]
    DATABASE_PORT: str = os.environ["DATABASE_PORT"]
    DATABASE_NAME: str = os.environ["DATABASE_NAME"]
    
    

settings = Settings()

def get_settings() -> Settings:
    return Settings
