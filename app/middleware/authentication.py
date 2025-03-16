from fastapi import Depends, HTTPException, status, Request, Response
from fastapi.security import APIKeyCookie
from app.utils.tokens import verify_token, create_access_token, send_token
from app.config.db_config import collection
from typing import Optional

# Cookie extractors
oauth2_scheme_access = APIKeyCookie(name="access_token", auto_error=False)
oauth2_scheme_refresh = APIKeyCookie(name="refresh_token", auto_error=False)

async def get_current_user(
    request: Request,
    response: Response,
    access_token: str = Depends(oauth2_scheme_access),
    refresh_token: str = Depends(oauth2_scheme_refresh),
) -> Optional[dict]:
    """
    Middleware that extracts and validates the user from authentication tokens.
    
    If access token is invalid but refresh token is valid, generates a new access token.
    """
    from utils.tokens import ACCESS_TOKEN_SECRET, REFRESH_TOKEN_SECRET
    
    # No tokens provided
    if not access_token and not refresh_token:
        return None
        
    # Try to validate access token
    if access_token:
        payload = verify_token(access_token, ACCESS_TOKEN_SECRET)
        if payload:
            user_id = payload.get("id")
            user = collection.find_one({"_id": user_id})
            if user:
                return user
    
    # Access token invalid or expired, try refresh token
    if refresh_token:
        payload = verify_token(refresh_token, REFRESH_TOKEN_SECRET)
        if payload:
            user_id = payload.get("id")
            user = collection.find_one({"_id": user_id})
            
            if user:
                # Generate new access token
                new_access_token = create_access_token({"id": str(user["_id"])})
                
                # Set the new access token in the response
                send_token(user, response)
                
                return user
    
    # Both tokens are invalid
    return None

async def require_auth(current_user: dict = Depends(get_current_user)):
    """
    Dependency that ensures a user is authenticated.
    Raises an exception if no valid user is found.
    """
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return current_user