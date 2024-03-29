

from typing import List
from fastapi import APIRouter, Body, Depends, File, Response
from sqlmodel.ext.asyncio.session import AsyncSession

from api.deps import get_current_user, get_db
from schema.item_schema import ItemSchema
from crud.item_crud import CRUDItem
from crud.user_crud import CRUDUser
from db.models.user_model import User
from schema.permission_schema import ROLE_PERMISSIONS, RoleEnum
from schema.user_schema import UserShow


router = APIRouter()


@router.get('/', response_description="admin retrieve all users")
async def get_all_users(
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user(RoleEnum.PRODUCER))
) -> List[UserShow] :
    
    return await CRUDUser(db_session).get_all_user()


@router.get('/{username}', response_description="admin retrieve user")
async def get_users(
    username: str,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user(RoleEnum.PRODUCER))
) -> UserShow:
    
    return await CRUDUser(db_session).get_by_username(username)

@router.get('/{username}/items', response_description="admin retrieve item by user ")
async def get_item_by_user(
    username: str,
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user(RoleEnum.PRODUCER))
) -> List[ItemSchema]:
    
    return await CRUDItem(db_session).get_items(username)
    
