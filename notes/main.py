from fastapi import APIRouter
from fastapi import Request

notes_router = APIRouter()

@notes_router.get("/", status_code=200)
async def Home(request: Request):
    return []

