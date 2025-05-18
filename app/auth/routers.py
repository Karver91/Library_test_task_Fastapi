from typing import Annotated

from fastapi import APIRouter, Depends
from starlette.status import HTTP_201_CREATED

from app.auth.schemas import UserResponse, UserCreate, Token
from app.auth.service import AuthService
from app.auth.utils import CustomOAuth2EmailRequestForm
from app.dependencies import auth_service

router = APIRouter(prefix="/auth", tags=["Аутентификация"])


@router.post(
    path="/register",
    response_model=UserResponse,
    status_code=HTTP_201_CREATED
)
async def register(
        user_data: UserCreate,
        service: Annotated[AuthService, Depends(auth_service)]
):
    return await service.register(data=user_data)


@router.post(
    path="/login",
    response_model=Token
)
async def login(
        service: Annotated[AuthService, Depends(auth_service)],
        user_data: CustomOAuth2EmailRequestForm = Depends()
):
    return await service.login(user_data)
