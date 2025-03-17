from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Response
from app.config.db_config import collection
from app.models.schema import all_users
from app.utils.tokens import send_token
from app.models.schema import UserCreate, UserUpdate, UserLogin, UserResponse
from app.models.schema import individual_user
import bcrypt
from bson import ObjectId  # Make sure this import is at the top


# Read User
async def read_user(user_id: str):
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(user_id)
        user = collection.find_one({"_id": object_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return individual_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# New User
async def create_user(data: UserCreate):
    try:
        email = data.email
        password = data.password
        full_name = data.full_name
        role = data.role

        if not email or not password or not full_name or not role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide all required fields: email, password, full_name, and role",
            )
        existing_user = collection.find_one({"email": email})
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

        user_data = data.dict()

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

        user_data["password"] = hashed_password
        result = collection.insert_one(user_data)
        created_user = collection.find_one({"_id": result.inserted_id})
        user_response = individual_user(created_user)

        user_response["password"] = None
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User created successfully", "data": user_response},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update User
async def update_user(user_id: str, data: UserUpdate):
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(user_id)
        existing_user = collection.find_one({"_id": object_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Filter out None values and convert to dict
        update_data = {k: v for k, v in data.dict().items() if v is not None}

        # Handle password hashing if present
        if "password" in update_data and update_data["password"]:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(
                update_data["password"].encode("utf-8"), salt
            )
            update_data["password"] = hashed_password

        # Update the document
        collection.update_one({"_id": object_id}, {"$set": update_data})

        # Get the updated user
        updated_user = collection.find_one({"_id": object_id})

        # Format the user data for response
        user_response = individual_user(updated_user)

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User updated successfully", "data": user_response},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete User
# Delete User
async def delete_user(user_id: str):
    try:
        # Convert string ID to ObjectId
        object_id = ObjectId(user_id)
        existing_user = collection.find_one({"_id": object_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        collection.delete_one({"_id": object_id})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User deleted successfully"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Login
async def login(data: UserLogin, response: Response):
    try:
        email = data.email
        password = data.password

        if not email or not password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Please provide email and password",
            )

        user = collection.find_one({"email": email})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if not bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password",
            )

        user_data = individual_user(user)

        return send_token(user_data, response, status_code=status.HTTP_200_OK)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Logout
async def logout(response: Response):
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Logged out successfully"},
    )
