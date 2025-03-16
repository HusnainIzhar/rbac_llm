from app.config.db_config import collection
from app.models.schema import all_users
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse


# Read Users
async def get_all_users():
    try:
        data = collection.find()
        return all_users(data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Bulk Delete Users
async def bulk_delete_users(user_ids: list):
    try:
        collection.delete_many({"_id": {"$in": user_ids}})
        return {"message": "Users deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Change Role
async def update_role(user_id, role_data: dict):
    try:
        user = collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        role = collection.update_one({"_id": user_id}, {"$set": role_data})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Role updated successfully", "data": role},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))