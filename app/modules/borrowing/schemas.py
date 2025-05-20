from datetime import datetime

from pydantic import BaseModel, PositiveInt, ConfigDict

from app.modules.book.schemas import BookWithID
from app.utils.schemas import BaseResponse


class BorrowingCreateScheme(BaseModel):
    book_id: PositiveInt
    reader_id: PositiveInt


class BorrowingCreateResponseScheme(BorrowingCreateScheme):
    id: PositiveInt
    borrow_date: datetime

    model_config = ConfigDict(from_attributes=True)


class BorrowingWithBook(BaseModel):
    id: PositiveInt
    borrow_date: datetime
    return_date: datetime | None
    book: BookWithID

    model_config = ConfigDict(from_attributes=True)


class BorrowingCreateResponse(BaseResponse):
    data: list[BorrowingCreateResponseScheme]
