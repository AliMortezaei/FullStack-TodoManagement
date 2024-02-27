from sqlmodel import SQLModel, Field, BINARY

from .base_model import BaseUUIDModel 
from .permissions import ModelPermissions

class ItemBase(SQLModel):
    name: str = Field(nullable=False, unique=True)
    discription: str | None = Field(default=None)

class Item(BaseUUIDModel, ItemBase, ModelPermissions, table=True):
    image: bytes = Field(BINARY)
    user: int = Field(foreign_key="user.id")