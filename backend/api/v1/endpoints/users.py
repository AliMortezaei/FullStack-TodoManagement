from typing import List

from fastapi import APIRouter, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.user_crud import CRUDUser
from api.deps import get_db, get_current_user
from db.models import User
from schema.user_schema import UserShow
from schema.role_schema import RoleEnum
from schema.permission_schema import UserPermission


router = APIRouter()

# @router.get("/list")
# async def user_list(
#     db_session: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user(RoleEnum.PRODUCER))
# ) -> List[UserShow] :
    
#     return await CRUDUser(db_session).get_all_user()

@router.get('/')
async def retierve_user_profile(
    db_session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user([UserPermission.permissions.READ]))   
) -> UserShow:
    return current_user

# async def update_user_profile(
#     db_session: AsyncSession = Depends(get_db), 

# ):





