from app.config.db_config import collection
from app.models.schema import all_users
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from bson import ObjectId
from app.models.schema import individual_user



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
        # Convert string IDs to ObjectId
        object_ids = [ObjectId(id) for id in user_ids]
        result = collection.delete_many({"_id": {"$in": object_ids}})
        return {"message": f"Users deleted successfully: {result.deleted_count} users removed"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Change Role
async def update_role(user_id, role_data):
    try:
        # Convert to dict if role_data is a Pydantic model
        if hasattr(role_data, "dict"):
            role_data = role_data.dict()
            
        # Convert string ID to ObjectId
        object_id = ObjectId(user_id)
        user = collection.find_one({"_id": object_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Update user role
        collection.update_one({"_id": object_id}, {"$set": role_data})
        
        # Get updated user
        updated_user = collection.find_one({"_id": object_id})
        user_response = individual_user(updated_user)
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Role updated successfully", "data": user_response},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))