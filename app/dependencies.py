from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_401_UNAUTHORIZED

from app.auth.models import User
from app.auth.repository import AuthRepository
from app.auth.service import AuthService
from app.db import get_async_session
from app.modules.book.repository import BookRepository
from app.modules.book.service import BookService
from app.modules.borrowing.repository import BorrowingRepository
from app.modules.borrowing.service import BorrowingService
from app.modules.reader.repository import ReaderRepository
from app.modules.reader.service import ReaderService

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


async def book_service(
        session: AsyncSession = Depends(get_async_session)
) -> BookService:
    return BookService(
        repository=BookRepository,
        session=session
    )


async def reader_service(
        session: AsyncSession = Depends(get_async_session)
) -> ReaderService:
    return ReaderService(
        repository=ReaderRepository,
        session=session
    )


async def borrowing_service(
        session: AsyncSession = Depends(get_async_session)
) -> BorrowingService:
    return BorrowingService(
        repository=BorrowingRepository,
        session=session
    )