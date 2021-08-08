from typing import List, Optional, Union

from app.models.pydantic import UserPayloadSchema, UserPostPayloadSchema, UserUpdatePayloadSchema
from app.models.tortoise import User
from app.core import get_password_hash

async def post(payload: UserPostPayloadSchema, hashed_password) -> int:

    user = User(
        username=payload.username,
        email=payload.email,
        full_name=payload.full_name,
        disabled=payload.disabled,
        hashed_password=hashed_password
    )
    await user.save()

    return user.id


async def get(id: int) -> Optional[dict]:
    user = await User.filter(id=id).first().values()
    if user:
        return user[0]
    return None


async def get_all() -> List:
    users = await User.all().values()
    return users


async def delete(id: int) -> int:
    user = await User.filter(id=id).first().delete()
    return user


async def put(id: int, payload: UserUpdatePayloadSchema) -> Union[dict, None]:
    hashed_password = await get_password_hash(payload.plain_password)
    user = await User.filter(id=id).update(username=payload.username, email=payload.email, full_name=payload.full_name, disabled=payload.full_name, hashed_password=hashed_password)
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user[0]
    return None
