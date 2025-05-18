from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from app.modules.book.models import Book
from app.modules.book.schemas import BookCreateScheme

URL_PREFIX = "/books/"


async def test_add_book(users, ac: AsyncClient, async_session: AsyncSession, books: list[Book]):
    amount = len(books)
    get_max_id = lambda lst: max(lst, key=lambda x: x.id).id
    max_book_id = get_max_id(books)
    payload = BookCreateScheme(
        name="some book",
        author="Some Author"
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_201_CREATED

    # Проверяем изменения в базе
    stmt = select(Book)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == amount + 1
    assert get_max_id(res) == max_book_id + 1
