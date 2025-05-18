from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings

engine = create_async_engine(settings.DATABASE_URL_asyncpg, echo=False)
async_session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    async def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.c}


async def get_async_session():
    async with async_session() as session:
        yield session
