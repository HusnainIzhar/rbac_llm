from fastapi import APIRouter, Depends
from app.controllers.admin_controller import get_all_users, bulk_delete_users, update_role
from app.middleware.role_checker import role_required
from app.middleware.authentication import require_auth
from typing import List
from pydantic import BaseModel
from app.models.schema import RoleUpdate  # Add this import


router = APIRouter(prefix="/admin", tags=["admin"])

class BulkDeleteRequest(BaseModel):
    user_ids: List[str]

@router.get("/users")
async def admin_get_all_users(current_user = Depends(role_required("admin"))):
    return await get_all_users()

@router.post("/users/bulk-delete")
async def admin_bulk_delete_users(
    request: BulkDeleteRequest,  # Use 'request' instead of 'user_ids'
    current_user: dict = Depends(role_required("admin"))
):
    return await bulk_delete_users(request.user_ids)  # Extract user_ids from request

@router.put("/users/{user_id}/role")
async def admin_assign_role(
    user_id: str,
    role_data: RoleUpdate,
    current_user: dict = Depends(role_required("admin"))
):
    # Convert the Pydantic model to a dictionary before passing to controller
    role_dict = role_data.dict()
    return await update_role(user_id, role_dict)