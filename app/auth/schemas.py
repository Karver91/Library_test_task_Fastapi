from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict

from app.utils.schemas import BaseResponse


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

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
