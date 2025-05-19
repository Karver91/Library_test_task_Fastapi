from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

from app.modules.reader.repository import ReaderRepository
from app.modules.reader.schemas import ReaderCreateScheme, ReaderResponse


class ReaderService:
    def __init__(
            self,
            repository: type[ReaderRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

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