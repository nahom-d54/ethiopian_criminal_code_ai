from fastapi import APIRouter
from src.routes.admin_routes import router as admin_route
from src.routes.chat_routes import chat_router

api_route = APIRouter(prefix="/api")

api_route.include_router(chat_router)
api_route.include_router(admin_route)
