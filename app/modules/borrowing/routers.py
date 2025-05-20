from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import PositiveInt
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.auth.models import User
from app.dependencies import user_dependency, borrowing_service
from app.modules.borrowing.schemas import BorrowingCreateScheme, BorrowingCreateResponse
from app.modules.borrowing.service import BorrowingService

router = APIRouter(prefix="/borrowing", tags=["Выдача книг"])


@router.post(
    path="/",
    response_model=BorrowingCreateResponse,
    status_code=HTTP_201_CREATED,
    summary="Выдать книгу"
)
async def borrow_book(
        request_info: BorrowingCreateScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BorrowingService, Depends(borrowing_service)]
):
    return await service.borrow_book(data=request_info)


@router.post(
    path="/{borrowing_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Вернуть книгу"
)
async def return_book(
        borrowing_id: PositiveInt,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BorrowingService, Depends(borrowing_service)]
):
    return await service.return_book(borrowing_id)
