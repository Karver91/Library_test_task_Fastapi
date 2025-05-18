from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.models import User
from app.auth.repository import AuthRepository
from app.auth.service import AuthService
from app.db import get_async_session

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login")  # это security scheme, который ищет токен в заголовке Authorization


async def auth_service(
        session: AsyncSession = Depends(get_async_session)
) -> AuthService:
    return AuthService(
        repository=AuthRepository,
        session=session
    )


async def user_dependency(
        service: Annotated[AuthService, Depends(auth_service)],
        token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    return await service.get_current_user(token)
