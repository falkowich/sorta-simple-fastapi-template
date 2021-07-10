from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.api import crud
from app.models.pydantic import (
    UserPayloadSchema,
    UserResponseSchema,
    UserUpdatePayloadSchema,
)
from app.models.tortoise import UserSchema

router = APIRouter()


@router.post("/", response_model=UserResponseSchema, status_code=201)
async def create_user(payload: UserPayloadSchema) -> UserResponseSchema:
    user_id = await crud.post(payload)

    response_object = {
        "id": user_id,
        "url": payload.url,
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
