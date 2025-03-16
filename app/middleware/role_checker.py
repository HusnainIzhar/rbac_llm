from fastapi import Depends, HTTPException, status
from typing import List, Union
from functools import wraps
from .authentication import get_current_user

def role_required(allowed_roles: Union[str, List[str]]):
    if isinstance(allowed_roles, str):
        allowed_roles = [allowed_roles]
        
    async def role_checker(current_user = Depends(get_current_user)):
        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Authentication required"
            )
        
        user_role = current_user.get("role")
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker