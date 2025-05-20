from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_400_BAD_REQUEST

from app.modules.book.repository import BookRepository
from app.modules.book.schemas import BookWithID
from app.modules.borrowing.repository import BorrowingRepository
from app.modules.borrowing.schemas import BorrowingCreateScheme, BorrowingResponse, BorrowingResponseScheme, \
    BorrowingCreateResponse
from app.modules.reader.schemas import ReaderWithID


class BorrowingService:
    def __init__(
            self,
            repository: type[BorrowingRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)


    async def create_borrowing(self, data: BorrowingCreateScheme):
        filters = {"reader_id": data.reader_id, "return_date": None}
        borrowed_books = await self.repository.get_by_filters(filters=filters)
        if len(borrowed_books) >= 3:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Читатель не может взять более 3ех книг")

        book_repository = BookRepository(session=self.repository.session)
        book = await book_repository.get_one(_id=data.book_id)
        if book.amount <= 0:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Книги нет в наличии")
        book.amount -= 1
        book_repository.session.add(book)
        await book_repository.session.commit()

        result = await self.repository.add_one(data=data.model_dump())

        return BorrowingCreateResponse(data=[result])
