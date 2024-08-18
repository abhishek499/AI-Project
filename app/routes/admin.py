# admin.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_user_role

router = APIRouter()

@router.get("/admin-only")
async def admin_only_route(role: str = Depends(get_user_role)):
    if role != "Admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return {"message": "Welcome, Admin!"}
