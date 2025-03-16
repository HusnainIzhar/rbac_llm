from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import Response
from config.db_config import collection
from models.schema import all_users
from utils.tokens import send_token
import bcrypt





# Read User
async def read_user(user_id: str):
    try:
        user = collection.find_one({"_id": user_id})
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# New User
async def create_user(data: dict):
    try:
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        role = data.get("role")

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

        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
        data["password"] = hashed_password

        user = collection.insert_one(data)
        user["password"] = None
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "User created successfully", "data": user},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Update User
async def update_user(user_id: str, data: dict):
    try:
        email = data.get("email")
        password = data.get("password")
        full_name = data.get("full_name")
        role = data.get("role")

        existing_user = collection.find_one({"_id": user_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        if password:
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
            data["password"] = hashed_password

        user = collection.update_one({"_id": user_id}, {"$set": data})
        user["password"] = None

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User updated successfully", "data": user},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Delete User
async def delete_user(user_id: str):
    try:
        existing_user = collection.find_one({"_id": user_id})
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        collection.delete_one({"_id": user_id})
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "User deleted successfully"},
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Login
async def login(data: dict, response: Response):
    try:
        email = data.get("email")
        password = data.get("password")

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

        user["password"] = None

        return send_token(user, response, status_code=status.HTTP_200_OK)
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
