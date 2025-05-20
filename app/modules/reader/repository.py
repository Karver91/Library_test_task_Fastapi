from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.borrowing.models import BorrowedBooks
from app.modules.reader.models import Reader
from app.utils.repository import SQLAlchemyRepository


class ReaderRepository(SQLAlchemyRepository):
    model = Reader

    def __init__(self, session):
        self.session = session

    async def get_reader_books(self, reader_id):
        stmt = (
            select(self.model)
            .where(self.model.id == reader_id)
            .options(
                selectinload(
                    self.model.borrowed_books.and_(
                        BorrowedBooks.return_date.is_(None)  # фильтр через and
                    )
                ).joinedload(BorrowedBooks.book)
            )
        )

        result = await self.session.execute(stmt)
        return result.unique().scalars().one()
