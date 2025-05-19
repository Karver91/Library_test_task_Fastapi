from typing import Annotated

from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import PositiveInt
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from app.auth.models import User
from app.dependencies import user_dependency, reader_service
from app.modules.reader.schemas import ReaderCreateScheme, ReaderResponse, ReaderScheme
from app.modules.reader.service import ReaderService

router = APIRouter(prefix="/readers")


@router.get(
    path="/",
    response_model=ReaderResponse,
    summary="Получить всех читателей"
)
async def get_all(
        user: Annotated[User, Depends(user_dependency)],
        service: Annotated[ReaderService, Depends(reader_service)]
):
    ...


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
    ...


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
    ...
