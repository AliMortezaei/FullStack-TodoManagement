from typing import List
from datetime import datetime

from fastapi import APIRouter, Body, Depends, Form, Request, UploadFile
from sqlmodel.ext.asyncio.session import AsyncSession

from crud.user_crud import CRUDUser
from api.deps import get_db, get_current_user, storage_file
from db.models import User
from schema.user_schema import UserShow, UserProfileUpdate
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


@router.put('/')
async def update_user_profile(
    image: UploadFile = Depends(storage_file),
    first_name: str = Form(default=None, description="first_name"),
    last_name: str = Form(default=None, description="last_naeme"),
    brithdate: datetime = Form(default=None, description="brithdate"),
    db_session: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user([UserPermission.permissions.READ]))   
) -> UserShow:
    user_profile = UserProfileUpdate(
        first_name=first_name, last_name=last_name,
        brithdate=brithdate, image=image
    )    
    return await CRUDUser(db_session).update(obj_current=current_user, data_in=user_profile)



