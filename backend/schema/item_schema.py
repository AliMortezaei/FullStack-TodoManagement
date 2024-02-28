

from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator

from db.models.user_model import User


class ItemSchema(BaseModel):
    id: int
    name: str 
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)
    
class ItemCreate(BaseModel):
    name: str 
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)
    user: int | str  

class ItemUpdate(BaseModel):
    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)

