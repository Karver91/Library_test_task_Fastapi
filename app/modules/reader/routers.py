from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import PositiveInt
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.auth.models import User
from app.dependencies import user_dependency, reader_service
from app.modules.reader.schemas import ReaderCreateScheme, ReaderResponse, ReaderScheme, ReaderWithBorrowingResponse
from app.modules.reader.service import ReaderService

router = APIRouter(prefix="/readers", tags=["Читатели"])


@router.get(
    path="/",
    response_model=ReaderResponse,
    summary="Получить всех читателей"
)
async def get_all(
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    return await service.get_all()


@router.post(
    path="/",
    response_model=ReaderResponse,
    status_code=HTTP_201_CREATED,
    summary="Добавить читателя"
)
async def add_one(
        request_info: ReaderCreateScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    return await service.add_one(data=request_info)


@router.patch(
    path="/{reader_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Обновить данные по читателю"
)
async def update_one(
        reader_id: PositiveInt,
        request_info: ReaderScheme,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    return await service.update_one(_id=reader_id, data=request_info)


@router.delete(
    path="/{reader_id}",
    status_code=HTTP_204_NO_CONTENT,
    summary="Удалить читателя"
)
async def delete_one(
        reader_id: PositiveInt,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    return await service.delete_one(_id=reader_id)


@router.get(
    path="/{reader_id}/books",
    response_model=ReaderWithBorrowingResponse,
    summary="Получить список всех невозвращенных книг читателя"
)
async def get_reader_books(
        reader_id: PositiveInt,
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    return await service.get_reader_books(_id=reader_id)
