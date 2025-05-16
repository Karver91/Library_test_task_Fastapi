from datetime import datetime

from sqlalchemy import ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BorrowedBooks(Base):
    __tablename__ = "borrowed"
    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )
    reader_id: Mapped[int] = mapped_column(
        ForeignKey("readers.id", onupdate="CASCADE", ondelete="CASCADE"), nullable=False
    )
    borrow_date: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    return_date: Mapped[datetime] = mapped_column(nullable=True, server_default=None)
