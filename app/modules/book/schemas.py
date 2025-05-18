from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from app.utils.schemas import BaseResponse


class BookScheme(BaseModel):
    name: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None
    isbn: Optional[str] = None
    amount: Optional[PositiveInt] = None


class BookCreateScheme(BookScheme):
    name: str
    author: str
    amount: PositiveInt = 1


class BookWithID(BookCreateScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


class BookUpdateScheme(BookScheme):
    pass


class BookResponse(BaseResponse):
    data: list[BookWithID]
