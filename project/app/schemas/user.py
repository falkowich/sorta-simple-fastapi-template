from pydantic import BaseModel, EmailStr, SecretStr, ValidationError, validator
from typing import Optional


class UserPayloadSchema(BaseModel):
    username: str
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    @validator("username")
    def username_alphanumeric(cls, v):
        assert v.isalnum(), "must be alphanumeric"
        return v


class UserPostPayloadSchema(UserPayloadSchema):
    plain_password: SecretStr

    @validator("plain_password")
    def password_minlenght(cls, v):
        passlength = len(v.get_secret_value())
        minlenght = 7
        if passlength < minlenght:
            v = False
        assert v, "must be atleast 8 characters"
        return v


class UserResponseSchema(UserPayloadSchema):
    id: int


class UserUpdatePayloadSchema(UserPayloadSchema):
    plain_password: SecretStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class UserInDB(UserPayloadSchema):
    hashed_password: str
