from enum import Enum

from pydantic import BaseModel


class RoleEnum(str, Enum):
    USER = "USER"
    PRODUCER = "PRODUCER"

    @classmethod
    def get_roles(cls):
        roles = list()
        for role in cls:
            roles.append(f"{role.value}")
        return roles

class RoleCreate(BaseModel):
    id: int | None
    name: str
    description: str

