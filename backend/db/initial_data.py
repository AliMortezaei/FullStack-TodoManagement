from re import T
from typing import List

from fastapi import Depends

from api.deps import get_db
from db.models.role_model import Role
from crud.crud_base import CRUDBase
from db.models.user_model import User
from schema.role_schema import RoleCreate
from core.config import settings
from api.deps import get_db
from core.security import PasswordHandler

roles_data: List[Role] = [
    Role(id= 0, name="USER", description="user role model normal"),
    Role(id= 1, name="PRODUCER", description="producer admin user model")
]

user_admin: User = User(
    id=1, 
    phone=settings.PRODUCER_PHONE,
    email=settings.PRODUCER_EMAIL,
    username=settings.PRODUCER_USERNAME,
    image=settings.DEFULT_IMAGE,
    is_active=True,
    first_name="admin",
    last_name="admin",
    role_id=1
)




async def initial_db(db):
    crud = CRUDBase(User, db)
    password_manager = PasswordHandler
    user = await crud.get_by_id(user_admin.id)
    if user:
        return None
    for role in roles_data:
        await CRUDBase(Role, db).create(role)
    password = password_manager.get_password_hash(settings.PRODUCER_PASSWORD)
    user_admin.password = password    
    await crud.create(user_admin)   
    

    
