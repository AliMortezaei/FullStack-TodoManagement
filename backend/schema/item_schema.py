

from fastapi import UploadFile
from pydantic import BaseModel, Field, model_validator

from db.models.user_model import User


class ItemSchema(BaseModel):
    id: int
    name: str 
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)
    
class ItemCreate(ItemSchema):
    name: str 
    description: str | None = Field(default=None)
    image: str | None = Field(default=None)
    user: int   

