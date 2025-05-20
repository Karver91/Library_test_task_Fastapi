from sqlalchemy import exists, select

from app.modules.book.models import Book
from app.utils.repository import SQLAlchemyRepository


class BookRepository(SQLAlchemyRepository):
    model = Book

    def __init__(self, session):
        self.session = session

    async def is_exists_by_author_title_year(
            self,
            author: str,
            title: str,
            year: int
    ):
        stmt = select(
            exists().where(
                self.model.name == title,
                self.model.author == author,
                self.model.year == year
            )
        )
        result = await self.session.scalar(stmt)
        return result