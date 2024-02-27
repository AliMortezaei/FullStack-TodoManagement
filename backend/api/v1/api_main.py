from fastapi import APIRouter
from .endpoints import authentication, users, items

api_router = APIRouter()

api_router.include_router(authentication.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/user/profile", tags=["profile"])
api_router.include_router(items.router, prefix="/user/items", tags=["items"])