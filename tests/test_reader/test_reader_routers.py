from random import choice

from httpx import AsyncClient
from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT, HTTP_200_OK

from app.modules.borrowing.models import BorrowedBooks
from app.modules.reader.models import Reader
from app.modules.reader.schemas import ReaderCreateScheme, ReaderScheme, ReaderWithBorrowingResponse

URL_PREFIX = "/readers/"


async def test_add_reader(ac: AsyncClient, async_session: AsyncSession, readers: list[Reader]):
    amount = len(readers)
    get_max_id = lambda lst: max(lst, key=lambda x: x.id).id
    max_reader_id = get_max_id(readers)
    payload = ReaderCreateScheme(
        email="com3523@example.com",
        name="Reader",
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_201_CREATED

    # Проверяем изменения в базе
    stmt = select(Reader)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == amount + 1
    assert get_max_id(res) == max_reader_id + 1


async def test_add_reader_400_email_is_exists(
        ac: AsyncClient, async_session: AsyncSession, readers: list[Reader]
):
    reader = choice(readers)
    payload = ReaderCreateScheme(
        email=reader.email,
        name="Reader",
    ).model_dump(mode="json")

    # вызываем ручку
    resp = await ac.post(url=URL_PREFIX, json=payload)
    assert resp.status_code == HTTP_400_BAD_REQUEST


async def test_update_reader(ac: AsyncClient, async_session: AsyncSession, readers: list[Reader]):
    reader = choice(readers)
    payload = ReaderScheme(
        name="Some Random Name"
    )

    # вызываем ручку
    resp = await ac.patch(url=f"{URL_PREFIX}{reader.id}", json=payload.model_dump(mode="json"))
    assert resp.status_code == HTTP_204_NO_CONTENT

    # Проверяем изменения в базе
    stmt = select(Reader).where(Reader.id == reader.id)
    res = (await async_session.execute(stmt)).scalars().one_or_none()
    assert res is not None
    assert res.name == payload.name


async def test_get_all_readers(async_session: AsyncSession, ac: AsyncClient, readers: list[Reader]):
    # вызываем ручку
    resp = await ac.get(url=URL_PREFIX)
    assert resp.status_code == HTTP_200_OK

    # Проверяем данные в ответе
    resp_data = resp.json()
    resp_models = sorted([Reader(**reader) for reader in resp_data['data']], key=lambda x: x.id)
    readers.sort(key=lambda x: x.id)
    assert len(resp_models) == len(readers)
    assert map(lambda x, y: x.id == y.id, zip(resp_models, readers))


async def test_delete_reader(async_session: AsyncSession, ac: AsyncClient, readers: list[Reader]):
    reader = readers[-1]

    # вызываем ручку
    resp = await ac.delete(url=f"{URL_PREFIX}{reader.id}")
    assert resp.status_code == HTTP_204_NO_CONTENT

    # Проверяем бд
    stmt = select(Reader)
    res = (await async_session.execute(stmt)).scalars().all()
    assert len(res) == len(readers) - 1

    stmt = select(exists().where(Reader.id == reader.id))
    res = await async_session.scalar(stmt)
    assert res is False


async def test_get_reader_books(async_session: AsyncSession, ac: AsyncClient, borrowing: list[BorrowedBooks]):
    borrow_record = choice(borrowing)
    reader_id = borrow_record.reader_id

    # вызываем ручку
    resp = await ac.get(url=f"{URL_PREFIX}{reader_id}/books")
    assert resp.status_code == HTTP_200_OK
    response_data = resp.json()
    data = ReaderWithBorrowingResponse(data=response_data['data']).data
    borrowed = data[0].borrowed_books
    for record in borrowed:
        assert record.return_date is None
