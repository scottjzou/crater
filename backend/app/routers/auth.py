from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.schemas import User
from app.services.supabase_client import supabase_client
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    try:
        # Verify token with Supabase
        response = supabase_client.get_client().auth.get_user(credentials.credentials)
        
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid authentication credentials")
        
        return User(
            id=response.user.id,
            email=response.user.email,
            name=response.user.user_metadata.get("name"),
            created_at=response.user.created_at
        )
    except Exception as e:
        logger.error(f"Authentication error: {e}")
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

@router.post("/logout")
async def logout():
    """Logout user"""
    try:
        supabase_client.get_client().auth.sign_out()
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        raise HTTPException(status_code=500, detail="Logout failed")
