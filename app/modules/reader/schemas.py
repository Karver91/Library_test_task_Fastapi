from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.utils.schemas import BaseResponse


class ReaderScheme(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None


class ReaderCreateScheme(ReaderScheme):
    name: str
    email: str


class ReaderWithID(ReaderCreateScheme):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ReaderResponse(BaseResponse):
    data: list[ReaderWithID]
