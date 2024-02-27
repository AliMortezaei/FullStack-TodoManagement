
from sqlmodel import SQLModel, Field, Relationship

from .base_model import BaseUUIDModel
from schema.role_schema import RoleEnum

class RoleBase(SQLModel):
    name: str = Field(nullable=False)
    discription: str

class Role(BaseUUIDModel ,RoleBase, table=True):
    users: list["User"] = Relationship(
        back_populates="role", sa_relationship_kwargs={"lazy": "selectin"}
    )



