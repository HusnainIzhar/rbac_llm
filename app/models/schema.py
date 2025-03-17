from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from bson import ObjectId

# Custom ObjectId field for MongoDB compatibility
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
        
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)
        
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# Helper functions for response formatting
def individual_user(user):
    return {
        "id": str(user["_id"]),
        "email": user.get("email", ""),
        "full_name": user.get("full_name", ""),
        "role": user.get("role", "user"),
        "created_at": user.get("created_at", 0)
    }

def all_users(users):
    return [individual_user(user) for user in users]

# Request Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "user"
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword",
                "full_name": "John Doe",
                "role": "user"
            }
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example": {
                "email": "updated@example.com",
                "full_name": "John Updated"
            }
        }

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
    class Config:
        schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword"
            }
        }

# Response Models
class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: int
    
    class Config:
        schema_extra = {
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "email": "user@example.com",
                "full_name": "John Doe",
                "role": "user",
                "created_at": 1647529634
            }
        }

# Query Models
class RagQuery(BaseModel):
    message: str
    
    class Config:
        schema_extra = {
            "example": {
                "message": "What information can you provide about this document?"
            }
        }

class RoleUpdate(BaseModel):
    role: str
    
    @validator('role')
    def validate_role(cls, v):
        allowed_roles = ["user", "admin", "moderator"]  # Add any other roles your system supports
        if v not in allowed_roles:
            raise ValueError(f"Role must be one of {allowed_roles}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "role": "admin"
            }
        }