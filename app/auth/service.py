from datetime import datetime, timezone, timedelta

import jwt
from fastapi import HTTPException
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED

from app.auth.models import User
from app.auth.repository import AuthRepository
from app.auth.schemas import UserCreate, UserResponse, JWTPayload, Token, TokenData
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    JWT_SECRET_KEY = settings.SECRET_KEY
    JWT_ALGORITHM = settings.ALGORITHM
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    def __init__(
            self,
            repository: type[AuthRepository],
            session: AsyncSession
    ):
        self.repository = repository(session=session)

    async def register(self, data: UserCreate):
        if await self.repository.get_user_by_email(email=data.email):
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Пользователь с таким email уже существует")
        data.hashed_password = await self.__get_password_hash(data.hashed_password)
        user = await self.repository.add_one(data.model_dump())
        return UserResponse(data=[user])

    async def login(self, data):
        user = await self.authenticate_user(email=data.username, password=data.password)
        if not user:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Неверный логин или пароль",
                headers={"WWW-Authenticate": "Bearer"}
            )
        payload = JWTPayload(
            sub=str(user.id),
            exp=None
        )
        access_token = await self.create_access_token(payload)
        return Token(access_token=access_token, token_type="bearer")


    async def get_current_user(self, token):
        credentials_exception = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.JWT_SECRET_KEY, algorithms=[self.JWT_ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(user_id=int(user_id))
        except InvalidTokenError:
            raise credentials_exception

        user = await self.repository.get_one(_id=token_data.user_id)
        if user is None:
            raise credentials_exception
        return user


    @staticmethod
    async def __get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    async def __verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    async def authenticate_user(self, email: str, password: str) -> User | bool:
        user: User = await self.repository.get_user_by_email(email=email)
        if user is None:
            return False
        if not await self.__verify_password(password, user.hashed_password):
            return False
        return user

    async def create_access_token(self, payload: JWTPayload) -> str:
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.exp = expire
        encode_jwt = jwt.encode(payload.model_dump(), self.JWT_SECRET_KEY, algorithm=self.JWT_ALGORITHM)
        return encode_jwt
