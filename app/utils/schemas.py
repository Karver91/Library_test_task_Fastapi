from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.enums import ResponseStatus


class BaseResponse(BaseModel):
    status: ResponseStatus = ResponseStatus.OK
    # message: Optional[str] = None
    data: Optional[list] = list()
