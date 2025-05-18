from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST

from app.modules.book.repository import BookRepository
from app.modules.book.schemas import BookCreateScheme, BookResponse, BookScheme


class BookService:
    def __init__(
            self,
            repository: type[BookRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def get_all(self):
        result = await self.repository.get_all()
        return BookResponse(data=result)

    async def add_one(self, data: BookCreateScheme):
        try:
            if await self.repository.is_exists_by_author_title_year(
                    author=data.author,
                    title=data.name,
                    year=data.year
            ):
                raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Книга уже существует")
            result = await self.repository.add_one(data.model_dump())
            if not result:
                raise
            return BookResponse(data=[result])
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


    async def update_one(self, _id, data: BookScheme):
        if not await self.repository.is_exists(_id=_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Книга c id: {_id} не найдена")
        data = data.model_dump(
            exclude_unset=True,
            exclude_none=True
        )
        return await self.repository.update_one(_id=_id, data=data)


    async def delete_one(self, _id):
        if not await self.repository.is_exists(_id=_id):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail=f"Книга c id: {_id} не найдена")
        return await self.repository.delete_one(_id=_id)
