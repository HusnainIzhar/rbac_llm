from fastapi import APIRouter, Depends
from controllers.admin_controller import get_all_users, bulk_delete_users, update_role
from middleware.role_checker import role_required
from middleware.authentication import require_auth

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/users", dependencies=[Depends(role_required("admin"), require_auth)])
async def admin_get_all_users():
    return await get_all_users()


@router.post(
    "/users/bulk-delete", dependencies=[Depends(role_required("admin"), require_auth)]
)
async def admin_bulk_delete_users(user_ids: list):
    return await bulk_delete_users(user_ids)


@router.put(
    "/users/{user_id}/role",
    dependencies=[Depends(role_required("admin"), require_auth)],
)
async def admin_assign_role(user_id: str, role_data: dict):
    return await update_role(user_id, role_data.get("role"))
