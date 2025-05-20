from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic.v1 import PositiveInt
from starlette.status import HTTP_201_CREATED

from app.auth.models import User
from app.dependencies import user_dependency, borrowing_service
from app.modules.borrowing.schemas import BorrowingCreateScheme, BorrowingResponse, BorrowingCreateResponse
from app.modules.borrowing.service import BorrowingService

router = APIRouter(prefix="/borrowing", tags=["Выдача книг"])


@router.post(
    path="/",
    response_model=BorrowingCreateResponse,
    status_code=HTTP_201_CREATED,
    summary="Выдать книгу"
)
async def create_borrowing(
        request_info: BorrowingCreateScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BorrowingService, Depends(borrowing_service)]
):
    return await service.create_borrowing(data=request_info)


@router.delete(
    path="/{borrowing_id}"
)
async def delete_borrowing(

):
    ...

# TODO: два метода POST и DELETE