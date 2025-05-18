from random import choice

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.modules.book.models import Book
from app.modules.book.schemas import BookCreateScheme, BookScheme

URL_PREFIX = "/books/"


async def test_add_book(ac: AsyncClient, async_session: AsyncSession, books: list[Book]):
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


async def test_update_book(ac: AsyncClient, async_session: AsyncSession, books: list[Book]):
    book = choice(books)
    payload = BookScheme(
        amount=2
    )

    # вызываем ручку
    resp = await ac.patch(url=f"{URL_PREFIX}{book.id}", json=payload.model_dump(mode="json"))
    assert resp.status_code == HTTP_204_NO_CONTENT

    # Проверяем изменения в базе
    stmt = select(Book).where(Book.id == book.id)
    res = (await async_session.execute(stmt)).scalars().one_or_none()
    assert res is not None
    assert res.amount == payload.amount


async def test_get_all_books(async_session: AsyncSession, ac: AsyncClient, books: list[Book]):
    # вызываем ручку
    resp = await ac.get(url=URL_PREFIX)
    assert resp.status_code == HTTP_200_OK

    # Проверяем данные в ответе
    resp_data = resp.json()
    resp_models = sorted([Book(**book) for book in resp_data['data']], key=lambda x: x.id)
    books.sort(key=lambda x: x.id)
    assert len(resp_models) == len(books)
    assert map(lambda x, y: x.id == y.id, zip(resp_models, books))
