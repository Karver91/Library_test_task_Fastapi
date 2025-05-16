from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    year: Mapped[int] = mapped_column(nullable=True)
    isbn: Mapped[str] = mapped_column(unique=True, nullable=True)
    amount: Mapped[int] = mapped_column(server_default="1", nullable=False)

    __table_args__ = (
        CheckConstraint("amount >= 0", name="check_amount_non_negative"),
    )
