from fastapi import APIRouter, HTTPException, status
from app.models import UserModel
from app.auth import get_password_hash
from app.database import user_collection

router = APIRouter()

@router.post("/create-user", response_model=UserModel)
async def create_user(user: UserModel):
    # Check if the user already exists
    existing_user = await user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the user's password
    user.password = get_password_hash(user.password)
    
    # Convert the user model to a dictionary and insert it into the database
    user_dict = user.dict(by_alias=True)
    await user_collection.insert_one(user_dict)
    del user.password
    
    # Return the user data (excluding the password)
    return user
