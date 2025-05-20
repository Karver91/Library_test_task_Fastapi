from abc import ABC, abstractmethod

from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import insert, select, delete, exists, update
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST


class AbstractRepository(ABC):
    @abstractmethod
    async def is_exists(self, _id):
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_filters(self, filters):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, _id):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, _id, data):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession = None):
        self.session = session

    async def is_exists(self, _id):
        stmt = select(exists().where(self.model.id == _id))
        result = await self.session.scalar(stmt)
        return result

    async def add_one(self, data: dict):
        try:
            stmt = insert(self.model).values(**data).returning(self.model)
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one()
        except IntegrityError as e:
            await self.session.rollback()
            if getattr(e, "orig", None) and (sqlstate := getattr(e.orig, "sqlstate", None)):
                match sqlstate:
                    case "23505":
                        raise HTTPException(
                            status_code=HTTP_400_BAD_REQUEST,
                            detail="Нарушение уникальности (UNIQUE constraint). Запись с таким значением уже есть в базе"
                        )
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise

    async def get_one(self, _id):
        stmt = select(self.model).where(self.model.id == _id)
        result = await self.session.execute(stmt)
        return result.scalars().one_or_none()

    async def get_all(self):
        stmt = select(self.model)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_filters(self, filters: dict):
        stmt = select(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_one(self, _id):
        try:
            stmt = delete(self.model).where(self.model.id == _id)
            await self.session.execute(stmt)
            await self.session.commit()
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise

    async def update_one(self, _id, data):
        try:
            stmt = update(self.model).where(self.model.id == _id).values(**data)
            await self.session.execute(stmt)
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            if getattr(e, "orig", None) and (sqlstate := getattr(e.orig, "sqlstate", None)):
                match sqlstate:
                    case "23505":
                        raise HTTPException(
                            status_code=HTTP_400_BAD_REQUEST,
                            detail="Нарушение уникальности (UNIQUE constraint). Запись с таким значением уже есть в базе"
                        )
            raise
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise
