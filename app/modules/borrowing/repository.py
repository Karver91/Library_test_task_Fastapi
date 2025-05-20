from app.modules.borrowing.models import BorrowedBooks
from app.utils.repository import SQLAlchemyRepository


class BorrowingRepository(SQLAlchemyRepository):
    model = BorrowedBooks

    def __init__(self, session):
        self.session = session
