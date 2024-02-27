
from pydantic import BaseModel, EmailStr
import secrets

class Settings(BaseModel):
    post: int = 80
    API_V1_STR: str = "/api/v1"
    ALLOWED_HOSTS: str = "localhost"
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db"
    SECRET_KEY: str = "test@asfwdv333dscc1233"
    EMAIL_kEY: str = b'testkey'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 1  
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 100  # 100 days
    EMAIL_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3 # 3 days
    DB_POOL_SIZE: int = 83
    # email config
    HOST: str = 'smtp.gmail.com'
    PORT: int = 587
    USERNAME: str = "mortezaei2324@gmail.com"
    PASSWORD: str = "sqvjjytcwivaihdq"
    SENDER: EmailStr = "mortezaei2324@gmail.com"
    # redis server
    REDIS_URL: str = "redis://127.0.0.1:6379"
    
settings = Settings()

def get_settings() -> Settings:
    return Settings
