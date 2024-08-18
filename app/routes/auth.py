from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from bson import ObjectId
from datetime import timedelta
from app.auth import get_password_hash, verify_password, create_access_token, get_current_user
from app.models import UserModel, UserLogin, UserResponse
from app.database import get_user_collection

router = APIRouter()

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserModel):
    user_collection = get_user_collection()
    existing_user = await user_collection.find_one({"email": user.email})
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    user_dict = user.dict()
    user_dict["password"] = hashed_password
    
    new_user = await user_collection.insert_one(user_dict)
    return UserResponse(email=user.email, role=user.role)

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_collection = get_user_collection()
    user = await user_collection.find_one({"email": form_data.username})
    

    print("User", user)
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user["email"], "role": user["role"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
