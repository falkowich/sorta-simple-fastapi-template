from pydantic import BaseModel
from typing import Optional


class UserPayloadSchema(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserPostPayloadSchema(UserPayloadSchema):
     plain_password: str

class UserResponseSchema(UserPostPayloadSchema):
    id: int

class UserUpdatePayloadSchema(UserPayloadSchema):
    plain_password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(UserPayloadSchema):
    hashed_password: str
