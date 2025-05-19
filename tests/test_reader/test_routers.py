from random import choice

from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.modules.reader.models import Reader
from app.modules.reader.schemas import ReaderCreateScheme

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
