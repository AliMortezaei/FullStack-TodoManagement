from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime

from sqlmodel import SQLModel, Field,BigInteger
from sqlalchemy.ext import declarative



class BaseUUIDModel(SQLModel):
    id: Optional[int] = Field(
        default=None,
        title="ID",
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True}
    )

    created_at: datetime = Field(
        default_factory= datetime.utcnow, nullable=False
        )
    updated_at: datetime = Field(
        default_factory= datetime.utcnow, 
        sa_column_kwargs={"onupdate": datetime.utcnow},
        nullable=False
        )

