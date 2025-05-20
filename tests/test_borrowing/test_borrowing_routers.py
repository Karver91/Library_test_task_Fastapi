from random import choice

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.modules.book.models import Book
from app.modules.borrowing.models import BorrowedBooks
from app.modules.borrowing.schemas import BorrowingCreateScheme
from app.modules.reader.models import Reader

URL_PREFIX = "/borrowing/"


async def test_borrow_book(
        async_session: AsyncSession,
        ac: AsyncClient,
        books: list[Book],
        readers: list[Reader]
):
    book = choice(books)
    book_id = book.id
    book_amount = book.amount
    reader_id = choice(readers).id
    payload = BorrowingCreateScheme(
        book_id=book_id,
        reader_id=reader_id
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_201_CREATED

    # Проверяем изменения в базе
    stmt = select(BorrowedBooks)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == 1

    stmt = select(Book).where(Book.id == book_id)
    res = (await async_session.execute(stmt)).scalars().one()
    assert res.amount == book_amount - 1


async def test_return_book(
        async_session: AsyncSession,
        ac: AsyncClient,
        borrowing: list[BorrowedBooks]
):
    borrow_record = choice(borrowing)
    book = await async_session.get_one(Book, borrow_record.book_id)
    book_amount = book.amount

    # вызываем ручку
    resp = await ac.post(url=f"{URL_PREFIX}{borrow_record.id}", params={"borrowing_id": borrow_record.id})
    assert resp.status_code == HTTP_204_NO_CONTENT

    # Проверяем изменения в базе
    stmt = select(BorrowedBooks).where(BorrowedBooks.id == borrow_record.id)
    res = (await async_session.execute(stmt)).scalars().one_or_none()
    assert res.return_date is not None

    stmt = select(Book).where(Book.id == borrow_record.book_id)
    res = (await async_session.execute(stmt)).scalars().one()
    assert res.amount == book_amount + 1
