from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import APIKeyCookie
from app.utils.tokens import verify_token, create_access_token, send_token
from app.config.db_config import collection
from typing import Optional
from app.utils.tokens import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET
from bson import ObjectId


oauth2_scheme_access = APIKeyCookie(name="access_token", auto_error=False)
oauth2_scheme_refresh = APIKeyCookie(name="refresh_token", auto_error=False)


async def get_current_user(
    request: Request,
    response: Response,
    access_token: str = Depends(oauth2_scheme_access),
    refresh_token: str = Depends(oauth2_scheme_refresh),
) -> Optional[dict]:

    if not access_token and not refresh_token:
        return None
    if access_token:
        payload = verify_token(access_token, ACCESS_TOKEN_SECRET)
        if payload:
            user_id = payload.get("id")
            try:
                user = collection.find_one({"_id": ObjectId(user_id)})
                if user:
                    return user
            except:
                pass

    if refresh_token:
        payload = verify_token(refresh_token, REFRESH_TOKEN_SECRET)
        if payload:
            user_id = payload.get("id")
            try:
                user = collection.find_one({"_id": ObjectId(user_id)})
                if user:
                    new_access_token = create_access_token({"id": str(user["_id"])})

                    response.set_cookie(
                        key="access_token",
                        value=new_access_token,
                        httponly=True,
                        max_age=3600,
                        expires=3600,
                        samesite="lax",
                        secure=False,
                    )

                    return user
            except:
                pass

    return None


async def require_auth(current_user: dict = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user
