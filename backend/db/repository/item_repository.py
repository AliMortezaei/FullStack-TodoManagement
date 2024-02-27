
from typing import Iterable
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.models.item_model import Item
from db.models.user_model import User




class ItemRepository():

    def __init__(self, db_session: AsyncSession) -> None:
        
        self.db_session = db_session

    async def get_item_all_by_user(self, user_id: int) -> Iterable[Item]:
        query = select(User, Item).join(Item).where(User.id == user_id)
        response = await self.db_session.execute(query)
        return [res.Item for res in response]

    async def get_item_by_user(self, user_id: int, item_id: int) -> Item | None:
        query = select(Item).join(User).where(Item.id == item_id, User.id == user_id)
        response = await self.db_session.execute(query)
        return response.scalar_one_or_none()