from typing import List, Optional, Union

from app.models.pydantic import UserPayloadSchema
from app.models.tortoise import User


async def post(payload: UserPayloadSchema) -> int:
    user = User(
        url=payload.url,
        name="dummy username",
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


async def put(id: int, payload: UserPayloadSchema) -> Union[dict, None]:
    user = await User.filter(id=id).update(url=payload.url, name=payload.name)
    if user:
        updated_user = await User.filter(id=id).first().values()
        return updated_user[0]
    return None
