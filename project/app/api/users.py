from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.pydantic import (
    UserPostPayloadSchema,
    UserResponseSchema,
    UserUpdatePayloadSchema,
)
from app.models.tortoise import UserSchema
from app.core import get_password_hash

router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(payload: UserPostPayloadSchema) -> UserResponseSchema:
    print(payload.plain_password)

    hashed_password = await get_password_hash(payload.plain_password)

    user_id = await crud.post(payload, hashed_password)

    response_object = {
        "id": user_id,
        "username": payload.username,
        "email": payload.email,
        "full_name": payload.full_name,
        "disabled": payload.disabled,
        "plain_password": hashed_password,
    }

    return response_object


@router.get("/{id}/", response_model=UserSchema)
async def read_user(id: int = Path(..., gt=0)) -> UserSchema:
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


@router.get("/", response_model=List[UserSchema])
async def read_all_users() -> List[UserSchema]:
    return await crud.get_all()


@router.delete("/{id}/", response_model=UserResponseSchema)
async def delete_user(id: int = Path(..., gt=0)) -> UserResponseSchema:
    user = await crud.get(id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await crud.delete(id)
    return user


@router.put("/{id}/", response_model=UserSchema)
async def update_user(
    payload: UserUpdatePayloadSchema, id: int = Path(..., gt=0)
) -> UserSchema:
    user = await crud.put(id, payload)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
