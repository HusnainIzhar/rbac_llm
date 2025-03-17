from fastapi import APIRouter, Depends, Response
from app.middleware.authentication import require_auth
from app.models.schema import UserCreate, UserUpdate, UserLogin, UserResponse

from app.controllers.user_controller import (
    create_user,
    update_user,
    delete_user,
    login,
    read_user,
    logout
)

router = APIRouter()

@router.get("/user/{user_id}", tags=["users"])
async def get_user(user_id: str, current_user = Depends(require_auth)):
    return await read_user(user_id)

@router.post("/create_user/", tags=["users"], response_model=UserResponse)
async def create_new_user(data: UserCreate):
    return await create_user(data)

@router.put("/update_user/{user_id}", tags=["users"])
async def update_existing_user(
    user_id: str, data: UserUpdate, current_user = Depends(require_auth)
):
    return await update_user(user_id, data)

@router.delete("/delete_user/{user_id}", tags=["users"])
async def delete_existing_user(user_id: str, current_user = Depends(require_auth)):
    return await delete_user(user_id)

@router.post("/login/", tags=["users"])
async def user_login(data: UserLogin, response: Response):
    return await login(data, response)

@router.post("/logout/", tags=["users"])
async def user_logout(response: Response, current_user = Depends(require_auth)):
    return await logout(response)
