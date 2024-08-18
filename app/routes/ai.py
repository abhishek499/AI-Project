from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from ..auth import get_current_user, get_user_role
from ..database import user_collection
import requests
from app.AI.search import search
from app.AI.summarize2 import summarizeUrls

router = APIRouter()

@router.post("/searchAboutAi")
async def search_about_ai(request:Request, user: dict = Depends(get_current_user), role: str = Depends(get_user_role)):
    body = await request.json();
    query = body.get("query");
    if role not in ["admin", "Member"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    

    urls = await search(query);

    summarize = await summarizeUrls(urls)
    

    return {"query": query, "results": urls, "summary": summarize}
