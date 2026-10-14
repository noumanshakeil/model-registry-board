from fastapi import APIRouter
from backend.api import health, registry, ui
api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(registry.router, prefix="/api", tags=["registry"])
api_router.include_router(ui.router, tags=["ui"])
