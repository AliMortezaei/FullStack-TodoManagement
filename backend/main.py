from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from celery import Celery
from sqlmodel import SQLModel


from api.v1.api_main import api_router
from core.config import settings
from db.session import engine
from db.session import SessionLocal

from db.initial_data import initial_db

def table_exists(table_name: str) -> bool:
    return table_name in {table.name for table in SQLModel.metadata.tables}


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(SQLModel.metadata.create_all)
        
    async with SessionLocal() as session:
        yield await initial_db(session)
    
    



app = FastAPI(lifespan=lifespan)


app.include_router(api_router, prefix= settings.API_V1_STR)


@app.get("/media/{item_name}", status_code=200, tags=['media'], description="show media file")
async def get_image(
    item_name: str,
):

    with open(f"media/{item_name}", "rb") as f:
        image_bytes = f.read()
    return Response(image_bytes, media_type="image/png")
