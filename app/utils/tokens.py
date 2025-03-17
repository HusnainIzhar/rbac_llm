from datetime import datetime, timedelta
from typing import Dict, Optional
from fastapi import Response, status
from jose import JWTError, jwt
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET") or "default_access_secret_key"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES") or "5")

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET") or "default_refresh_secret_key"
REFRESH_TOKEN_EXPIRE_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS") or "30")

IS_DEVELOPMENT = os.getenv("ENVIRONMENT") == "development"


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, REFRESH_TOKEN_SECRET, algorithm="HS256")
    return encoded_jwt


def verify_token(token: str, secret_key: str) -> Dict:
    try:
        payload = jwt.decode(token, secret_key, algorithms=["HS256"])
        return payload
    except JWTError:
        return None


def send_token(user: dict, response: Response, status_code: int = status.HTTP_200_OK):
    # Change this line:
    # From: access_token = create_access_token({"id": str(user["_id"])})
    # To:
    access_token = create_access_token({"id": user["id"]})
    
    # Change this line:
    # From: refresh_token = create_refresh_token({"id": str(user["_id"])})
    # To:
    refresh_token = create_refresh_token({"id": user["id"]})

    # Rest of function remains the same
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        expires=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=not IS_DEVELOPMENT,
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        expires=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax",
        secure=not IS_DEVELOPMENT,
    )

    if "password" in user:
        user_data = {k: v for k, v in user.items() if k != "password"}
    else:
        user_data = user

    return {"success": True, "access_token": access_token, "user": user_data}