from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.pool import NullPool, QueuePool
from sqlalchemy.engine.url import URL

from core.config import settings

db_url = URL.create(
    "postgresql+asyncpg",
    username= settings.POSTGRES_USER,
    password= settings.POSTGRES_PASSWORD,
    host= settings.POSTGRES_HOST,
    port= settings.POSTGRES_PORT,
    database= settings.POSTGRES_DB,
)

engine = create_async_engine(
    url= db_url,
    echo=False,
    future=True,
    poolclass=NullPool

    )

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    )