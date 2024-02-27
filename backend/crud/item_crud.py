
import shutil
from typing import List

from fastapi import HTTPException
from sqlmodel import select
from crud.crud_base import CRUDBase
from db.models.item_model import Item
from db.models.user_model import User
from schema.item_schema import ItemCreate, ItemSchema, ItemUpdate
from utils.context_manager import StorageLocalFile
from core.config import settings
from db.repository.item_repository import ItemRepository


class CRUDItem(CRUDBase[Item, ItemCreate]):
    
    def __init__(self, db_session):
        super().__init__(Item , db_session)
        self.adapter = ItemRepository(db_session)

    async def create_item(self, data_in: ItemCreate) -> ItemSchema:
        
        obj_data = Item.model_validate(data_in)
        return await self.create(obj_data)

    async def get_items(self, user: int | str = None) -> List[ItemSchema]:
        match type(user):
            case None:
                pass
            case int: 
                item = await self.adapter.get_item_all_by_user(user)
                if not  item:
                    raise HTTPException(status_code=404, detail="not found")
                return item

    async def get_item(self, item_id: int, user_id: int = None):
        match type(user_id):
            case None:
                pass
            case int:
                item = await self.adapter.get_item_by_user(user_id, item_id)
               # item.image = f"http://{settings.ALLOWED_HOSTS}/{(item.image).decode()}"
                if item is None:
                    raise HTTPException(status_code=404, detail="Item not found")
                return item



        


            