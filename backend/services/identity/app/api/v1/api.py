from api.v1.endpoints import login, register
from fastapi import APIRouter

apiv1_router = APIRouter()

apiv1_router.include_router(register.router, prefix="", tags=["Registration (Sign-Up)"])

apiv1_router.include_router(login.router, prefix="", tags=["Authentication (Sign-In)"])
