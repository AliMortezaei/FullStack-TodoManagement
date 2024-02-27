from enum import Enum




class RoleEnum(str, Enum):
    USER = "USER"
    PRODUCER = "PRODUCER"

    @classmethod
    def get_roles(cls):
        roles = list()
        for role in cls:
            roles.append(f"{role.value}")
        return roles





