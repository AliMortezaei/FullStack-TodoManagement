from fastapi import FastAPI, Response
from celery import Celery


from api.v1.api_main import api_router
from core.config import settings

app = FastAPI()


app.include_router(api_router, prefix= settings.API_V1_STR)


@app.get("/media/{item_name}", status_code=200, tags=['media'], description="show media file")
async def get_image(
    item_name: str,
):

    with open(f"media/{item_name}", "rb") as f:
        image_bytes = f.read()
    return Response(image_bytes, media_type="image/png")
