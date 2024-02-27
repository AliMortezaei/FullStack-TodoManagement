import shutil
from typing import Any, Iterable, List, Annotated
from collections.abc import AsyncGenerator

from jose import  JWTError, jwt, ExpiredSignatureError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, Header, HTTPException, UploadFile, status, File
from sqlmodel.ext.asyncio.session import AsyncSession

from schema.role_schema import RoleEnum
from schema.permission_schema import get_role_permissions
from schema.token_schema import TokenType
from schema.user_schema import IUserCreate
from db.session import SessionLocal
from core.redis import RedisManager, get_redis_db
from core.security import TokenFactory
from crud.user_crud import CRUDUser
from core.config import settings
from db.models.permissions import ModelPermission
from utils.context_manager import StorageLocalFile



http_bearer = HTTPBearer(bearerFormat="Bearer token",description="input token Beear" )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session

 
def get_header(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer)
):  
    if (credentials.scheme != "Bearer") and (not credentials.credentials):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid Header")
    return credentials.credentials




def get_current_user(
    required_permission: List[ModelPermission] | RoleEnum = None
):
    async def current_user(
        access_token: str = Depends(get_header),
        redis_client: RedisManager = Depends(get_redis_db),
        db_session: AsyncSession = Depends(get_db)
    ):
        
        try:
            pyload = TokenFactory()._decode(access_token)
            assert pyload["type"] == TokenType.ACCESS_TOKEN.value
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Your token has expired. Please log in again.",
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Error when decoding the token. Please check your request.",
            )
        except Exception as exp:
            raise HTTPException(
                status_code= status.HTTP_403_FORBIDDEN,
                detail="Invalied Token"
            )
            
        user_id = pyload['sub']
        token = redis_client.get_token_redis(user_id, TokenType.ACCESS_TOKEN.value)
        if (not user_id) or token is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN , detail='invalid user')

        user = await CRUDUser(db_session).get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail='User not found')
        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail='Inactive User')
        print(required_permission   )
        roles_validate = permission_checker(required_permission, user.role.name)
        if roles_validate is False:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this resource"
            )
        return user
    
    return current_user

    

def storage_file(
    image: UploadFile = File(default=None, description="media image")
):
    if image is not None:
        with StorageLocalFile(image.filename) as f:
            shutil.copyfileobj(image.file, f)
        return f.name

def permission_checker(
    required_permissions: List[ModelPermission] | RoleEnum, user_role: str
): 
    if type(required_permissions) is RoleEnum:
        required_permissions = get_role_permissions(required_permissions)
    # print(type(required_permissions))
    roles = get_role_permissions(user_role)
    for i in range(0,len(roles)):
        for permission in required_permissions:
            if str(permission) == str(roles[i]):
                return True

    return False








     