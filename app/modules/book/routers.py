from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.auth.models import User
from app.dependencies import book_service, user_dependency
from app.modules.book.schemas import BookCreateScheme, BookResponse
from app.modules.book.service import BookService

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get(
    path="/"
)
async def get_all():
    # TODO: вернуть с id и количеством книг
    ...


@router.post(
    path="/",
    response_model=BookResponse,
    status_code=HTTP_201_CREATED,
    summary="Добавить книгу"
)
async def add_one(
        request_info: BookCreateScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BookService, Depends(book_service)]
):
    return await service.add_one(data=request_info)


@router.patch(
    path="/{book_id}"
)
async def update_one():
    ...


@router.delete(
    path="/{book_id}"
)
async def delete_one():
    ...

# разделить логику для добавления количества книг и добавления новой книги с новым автором или названием
