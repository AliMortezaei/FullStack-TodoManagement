
import shutil
from typing import List

from sqlmodel import select
from crud.crud_base import CRUDBase
from db.models.item_model import Item
from db.models.user_model import User
from schema.item_schema import ItemCreate, ItemSchema
from utils.context_manager import StorageLocalFile
from db.repository.item_repository import ItemRepository


class CRUDItem(CRUDBase[Item, ItemCreate]):
    
    def __init__(self, db_session):
        super().__init__(Item , db_session)
        self.adapter = ItemRepository(db_session)

    async def create_item(self, data_in: ItemCreate) -> ItemSchema:
        
        obj_data = Item.model_validate(data_in)
        return await self.create(obj_data)

    async def get_items(self, user_id: int = None) -> List[ItemSchema]:
        match user_id:
            case None:
                pass
            case int: 
                return await self.adapter.get_item_all_by_user(user_id)
        