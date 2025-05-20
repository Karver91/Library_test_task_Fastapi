from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt, ConfigDict, Field, AliasPath

from app.modules.book.schemas import BookWithID
from app.modules.reader.schemas import ReaderWithID
from app.utils.schemas import BaseResponse


class BorrowingCreateScheme(BaseModel):
    book_id: PositiveInt
    reader_id: PositiveInt

class BorrowingCreateResponseScheme(BorrowingCreateScheme):
    id: PositiveInt
    borrow_date: datetime

    model_config = ConfigDict(from_attributes=True)


class BorrowingResponseScheme(BaseModel):
    id: PositiveInt
    book: BookWithID
    reader: ReaderWithID
    borrow_date: datetime
    return_date: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class BorrowingResponse(BaseResponse):
    data: list[BorrowingResponseScheme]

class BorrowingCreateResponse(BaseResponse):
    data: list[BorrowingCreateResponseScheme]
