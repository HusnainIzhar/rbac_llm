from fastapi import APIRouter, Depends
from app.controllers.admin_controller import get_all_users, bulk_delete_users, update_role
from app.middleware.role_checker import role_required
from app.middleware.authentication import require_auth

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users")
async def admin_get_all_users(current_user = Depends(role_required("admin"))):
    return await get_all_users()


@router.post("/users/bulk-delete")
async def admin_bulk_delete_users(user_ids: list, current_user = Depends(role_required("admin"))):
    return await bulk_delete_users(user_ids)


@router.put("/users/{user_id}/role")
async def admin_assign_role(user_id: str, role_data: dict, current_user = Depends(role_required("admin"))):
    return await update_role(user_id, role_data)