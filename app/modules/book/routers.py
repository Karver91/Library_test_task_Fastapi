from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.auth.models import User
from app.dependencies import book_service, user_dependency
from app.modules.book.schemas import BookCreateScheme, BookResponse, BookScheme
from app.modules.book.service import BookService

router = APIRouter(prefix="/books", tags=["Книги"])


@router.get(
    path="/",
    response_model=BookResponse,
    summary="Получить все книги"
)
async def get_all(
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BookService, Depends(book_service)]
):
    return await service.get_all()


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
    path="/{book_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Обновить данные по книге"
)
async def update_one(
        book_id: int,
        request_info: BookScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[BookService, Depends(book_service)]
):
    return await service.update_one(_id=book_id, data=request_info)


@router.delete(
    path="/{book_id}"
)
async def delete_one():
    ...

# разделить логику для добавления количества книг и добавления новой книги с новым автором или названием
