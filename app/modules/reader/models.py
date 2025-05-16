from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db import Base


class Reader(Base):
    __tablename__ = "readers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
