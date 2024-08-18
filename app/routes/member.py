# member.py
from fastapi import APIRouter, Depends, HTTPException, status
from app.auth import get_user_role

router = APIRouter()

@router.get("/member-only")
async def member_only_route(role: str = Depends(get_user_role)):
    if role != "Member":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return {"message": "Welcome, Member!"}
