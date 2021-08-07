from pydantic import BaseModel
from typing import Optional


class UserPayloadSchema(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserResponseSchema(UserPayloadSchema):
    id: int


class UserUpdatePayloadSchema(UserPayloadSchema):
    name: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(UserPayloadSchema):
    hashed_password: str
