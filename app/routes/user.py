from fastapi import APIRouter, Depends
from middleware.authentication import require_auth
from controllers.user_controller import (
    create_user,
    update_user,
    delete_user,
    login,
    read_user,
)

router = APIRouter()

@router.get("/user/{user_id}", tags=["users"])
async def get_user(user_id: str, dependencies=[Depends(require_auth)]):
    return await read_user(user_id)

@router.post("/create_user/", tags=["users"])
async def create_new_user(data: dict):
    return await create_user(data)

@router.put("/update_user/{user_id}", tags=["users"])
async def update_existing_user(
    user_id: str, data: dict, dependencies=[Depends(require_auth)]
):
    return await update_user(user_id, data)

@router.delete("/delete_user/{user_id}", tags=["users"])
async def delete_existing_user(user_id: str, dependencies=[Depends(require_auth)]):
    return await delete_user(user_id)

@router.post("/login/", tags=["users"])
async def user_login(data: dict, dependencies=[Depends(require_auth)]):
    return await login(data)
