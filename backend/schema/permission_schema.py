
from db.models.permissions import ModelPermissions
from schema.role_schema import RoleEnum


class UserPermission(ModelPermissions):
    pass

class ItemPermission(ModelPermissions):
    pass



ROLE_ENUM_PERMISSIONS = {
    RoleEnum.PRODUCER: [
        [
            UserPermission.permissions.CREATE,
            UserPermission.permissions.READ,
            UserPermission.permissions.UPDATE,
            UserPermission.permissions.DELETE
        ],
        [
            ItemPermission.permissions.CREATE,
            ItemPermission.permissions.READ,
            ItemPermission.permissions.UPDATE,
            ItemPermission.permissions.DELETE
        ]
    ],
    RoleEnum.USER: [
        [
            UserPermission.permissions.READ,

        ],
        [
            ItemPermission.permissions.CREATE,
            ItemPermission.permissions.READ,
            ItemPermission.permissions.UPDATE,
            ItemPermission.permissions.DELETE
        ]
    ]
}

def get_role_permissions(role: RoleEnum):
    permissions = set()
    for permissions_group in ROLE_ENUM_PERMISSIONS[role]:
        for permission in permissions_group:
            permissions.add(str(permission))
    return list(permissions)