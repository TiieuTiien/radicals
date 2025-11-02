from fastapi import APIRouter

from api.routes import words

api_router = APIRouter()

api_router.include_router(words.router)