from datetime import datetime
from random import choice

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.auth.models import User
from app.config import settings
from app.db import Base, get_async_session
from app.dependencies import user_dependency
from app.main import app
from app.modules.book.models import Book
from app.modules.borrowing.models import BorrowedBooks
from app.modules.reader.models import Reader


@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_engine():
    engine = create_async_engine(url=settings.DATABASE_URL_asyncpg, echo=True, poolclass=NullPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(async_engine):
    async_session_factory = async_sessionmaker(bind=async_engine, expire_on_commit=False)
    async with async_session_factory() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture(scope="function")
async def ac(async_session: AsyncSession, users: User):
    async def mok_user():
        return choice(users)

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000/") as ac:
        app.dependency_overrides[get_async_session] = lambda: async_session
        app.dependency_overrides[user_dependency] = mok_user
        yield ac
        app.dependency_overrides = {}


@pytest_asyncio.fixture(scope="function")
async def users(async_session: AsyncSession) -> list[User]:
    users_lst = [
        User(
            id=i,
            email=f"user_{i}@test.com",
            hashed_password='password',
            created_at=datetime.now()
        ) for i in range(1, 4)
    ]
    async_session.add_all(users_lst)
    await async_session.flush()
    return users_lst


@pytest_asyncio.fixture(scope="function")
async def books(async_session: AsyncSession) -> list[Book]:
    authors = ["А.С Пушкин", "Л.Н. Толстой", "А.П. Чехов"]
    books = [
        Book(
            name=f"Book_{i}",
            author=authors[i],
            year=1990 + i,
            amount=1
        ) for i in range(len(authors))
    ]
    async_session.add_all(books)
    await async_session.flush()
    return books


@pytest_asyncio.fixture(scope="function")
async def readers(async_session: AsyncSession) -> list[Reader]:
    readers = [
        Reader(
            name=f"Reader_{i}",
            email=f"reader{i}@text.com"
        ) for i in range(1, 4)
    ]
    async_session.add_all(readers)
    await async_session.flush()
    return readers


@pytest_asyncio.fixture(scope="function")
async def borrowing(
        async_session: AsyncSession,
        books: list[Book],
        readers: list[Reader]
) -> list[BorrowedBooks]:
    book_id = choice(books).id
    reader_id = choice(readers).id
    borrowing = [
        BorrowedBooks(
            book_id=book_id,
            reader_id=reader_id
        )
    ]
    async_session.add_all(borrowing)
    await async_session.flush()
    return borrowing
