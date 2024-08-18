from fastapi import FastAPI
from app.routes import auth, admin, member, user, ai
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(member.router, prefix="/member", tags=["member"])
app.include_router(user.router, prefix="/user", tags=["user"])
app.include_router(ai.router, prefix="/ai", tags=["ai"]) 

@app.get("/")
async def root():
    return {"message": "Welcome to the secure FastAPI app!"}