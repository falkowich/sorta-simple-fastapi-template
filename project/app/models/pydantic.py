from pydantic import AnyHttpUrl, BaseModel


class UserPayloadSchema(BaseModel):
    url: AnyHttpUrl


class UserResponseSchema(UserPayloadSchema):
    id: int


class UserUpdatePayloadSchema(UserPayloadSchema):
    name: str
