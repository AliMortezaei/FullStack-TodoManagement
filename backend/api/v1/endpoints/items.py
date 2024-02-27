

from typing import List
from fastapi import APIRouter, Body, Depends, File, Response, UploadFile, Form
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models.item_model import Item
from crud.crud_base import CRUDBase
from crud.item_crud import CRUDItem
from schema.permission_schema import ItemPermission
from api.deps import get_current_user, get_db, storage_file
from schema.item_schema import ItemCreate, ItemSchema, ItemUpdate
from db.models import User


router = APIRouter()



@router.post("/", status_code=201)
async def create_item(
    name: str = Form(description="name for item"),
    description: str = Form(default=None, description="description for item"),    
    image: UploadFile = Depends(storage_file),
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user([ItemPermission.permissions.CREATE]))   
) -> ItemSchema:

    item = ItemCreate(name=name, description=description, image=image, user=current_user.id)    
    return await CRUDItem(db_session).create_item(item)

@router.get("/", status_code=200, response_description='get all item for user')
async def get_items(
    db_session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user([ItemPermission.permissions.READ]))   
) -> List[ItemSchema]:

    return await CRUDItem(db_session).get_items(current_user.id)


@router.delete("/{item_id}", status_code=204, response_description='deleted item')
async def delete_item(
    item_id: int,
    current_user: User = Depends(get_current_user([
        ItemPermission.permissions.READ, ItemPermission.permissions.DELETE
    ])),
    db_session: AsyncSession = Depends(get_db),
) -> Response:
    crud = CRUDItem(db_session)
    item = await crud.get_item(item_id, current_user.id)

    return await crud.remove(id=item.id)

@router.put('/')
async def update_item(
    item_id: int,
    name: str = Form(default=None, description="name for item in update"),
    description: str = Form(default=None, description="description for item in update"),    
    image: UploadFile = Depends(storage_file),
    current_user: User = Depends(get_current_user([
        ItemPermission.permissions.READ, ItemPermission.permissions.DELETE, ItemPermission.permissions.UPDATE
    ])),
    db_session: AsyncSession = Depends(get_db),
) -> ItemSchema:

    crud = CRUDItem(db_session)
    item = await crud.get_item(item_id, current_user.id)

    return await crud.update(
        obj_current=item,
        data_in=ItemUpdate(name=name, description=description, image=image)
    )










