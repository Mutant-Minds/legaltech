from api.v1.endpoints import register
from fastapi import APIRouter

apiv1_router = APIRouter()

apiv1_router.include_router(register.router, prefix="", tags=["Register"])
