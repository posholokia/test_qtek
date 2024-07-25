from fastapi import APIRouter

from .account.handlers import router as account_router


router = APIRouter(prefix="/v1")


router.include_router(account_router, tags=["Users"])
