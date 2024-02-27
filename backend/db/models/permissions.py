import re
from enum import Enum
from typing import Type, List

from schema.role_schema import RoleEnum 


class Permission:

    def __init__(self, permission_type: str):
        self.permission_type = str(permission_type)

    def __str__(self):
        return self.permission_type

    def __eq__(self, other):
        if(
            isinstance(other, str) 
            or isinstance(other, Permission)
            or issubclass(Permission)
        ):  
            return self.permission_type == str(other)
        return False

class PermissionType(str, Enum):

    CREATE = "CREATE"
    READ = "READ"
    UPDATE = "UPDATE"
    DELETE = "DELETE"

    def __str__(self):
        return f"{self.value}"

class ModelPermission(Permission):

    def __init__(self, permission_type: PermissionType, permission_model: Type):

        self.permission_type = permission_type
        self.permission_model = permission_model

    def __str__(self):
        model_name = re.sub(
            r"(?<!^)(?=[A-Z])", "_", self.permission_model.__name__
        ).upper()
        return f"{model_name}_{self.permission_type.__str__().upper()}"


class ModelDefaultPermissions:
    """
        Class that provides a set of default permissions used by a model.
        It is used by the ModelPermissions class.
    """
    def __init__(self, model):
        self.CREATE = ModelPermission(
            permission_type=PermissionType.CREATE, permission_model=model
        )
        self.READ = ModelPermission(
            permission_type=PermissionType.READ, permission_model=model
        )
        self.UPDATE = ModelPermission(
            permission_type=PermissionType.UPDATE, permission_model=model
        )
        self.DELETE = ModelPermission(
            permission_type=PermissionType.DELETE, permission_model=model
        )

class ModelPermissions:
    """
    Provides the default set of permissions
    under the `permissions` attribute.
    """

    @classmethod
    @property
    def permissions(cls) -> ModelDefaultPermissions: # noqa
        return ModelDefaultPermissions(cls)
    

















    