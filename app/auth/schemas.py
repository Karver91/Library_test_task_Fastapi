from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict, Field

from app.utils.schemas import BaseResponse


class UserBase(BaseModel):
    email: EmailStr
    created_at: datetime


class UserCreate(BaseModel):
    email: EmailStr
    hashed_password: str = Field(alias="password")


class UserLogin(BaseModel):
    email: EmailStr
    hashed_password: str = Field(alias="password")


class UserWithID(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserResponse(BaseResponse):
    data: list[UserWithID]


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class JWTPayload(BaseModel):
    sub: str
    exp: Optional[str]
