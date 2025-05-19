from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.modules.reader.repository import ReaderRepository
from app.modules.reader.schemas import ReaderCreateScheme, ReaderResponse, ReaderScheme


class ReaderService:
    def __init__(
            self,
            repository: type[ReaderRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def get_all(self):
        result = await self.repository.get_all()
        return ReaderResponse(data=result)

    async def add_one(self, data: ReaderCreateScheme):
        try:
            result = await self.repository.add_one(data.model_dump())
            if not result:
                raise
            return ReaderResponse(data=[result])
        except HTTPException as http_exp:
            # logger.exception(http_exp.detail)
            raise http_exp
        except Exception as e:
            err_msg = "Ошибка добавления книги"
            # logger.exception(err_msg)
            raise HTTPException(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                detail=err_msg
            )

    async def update_one(self, _id, data: ReaderScheme):
        if not await self.repository.is_exists(_id=_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Читатель c id: {_id} не найден")
        data = data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )
        return await self.repository.update_one(_id=_id, data=data)
