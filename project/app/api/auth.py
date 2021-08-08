from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core import UserPayloadSchema, get_current_active_user, ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, timedelta, create_access_token
from app.models.pydantic import Token

router = APIRouter()


@router.get("/items/")
async def read_own_items(current_user: UserPayloadSchema = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]


@router.get("/me/", response_model=UserPayloadSchema)
async def read_users_me(current_user: UserPayloadSchema = Depends(get_current_active_user)):
    return current_user

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = await create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}