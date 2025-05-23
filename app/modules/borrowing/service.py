from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from app.modules.book.repository import BookRepository
from app.modules.borrowing.repository import BorrowingRepository
from app.modules.borrowing.schemas import BorrowingCreateScheme, \
    BorrowingCreateResponse


class BorrowingService:
    def __init__(
            self,
            repository: type[BorrowingRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)


    async def borrow_book(self, data: BorrowingCreateScheme):
        filters = {"reader_id": data.reader_id, "return_date": None}
        borrowed_books = await self.repository.get_by_filters(filters=filters)
        if len(borrowed_books) >= 3:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Читатель не может взять более 3ех книг")

        book_repository = BookRepository(session=self.repository.session)
        book = await book_repository.get_one(_id=data.book_id)
        if book.amount <= 0:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Книги нет в наличии")
        book.amount -= 1
        await self.repository.session.commit()

        result = await self.repository.add_one(data=data.model_dump())

        return BorrowingCreateResponse(data=[result])


    async def return_book(self, borrowing_id: int):
        borrowing = await self.repository.get_one(_id=borrowing_id)
        if borrowing is None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Не найдено записей в базе")
        if borrowing.return_date is not None:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Книга уже была возвращена")
        borrowing.return_date = datetime.now()
        book_repository = BookRepository(session=self.repository.session)
        book = await book_repository.get_one(_id=borrowing.book_id)
        book.amount += 1
        await self.repository.session.commit()
        return True
