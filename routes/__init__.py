from fastapi import APIRouter

from .ai_utilities import ai_utilities_router
from .authentication import authentication_router

router = APIRouter()

router.include_router(ai_utilities_router, prefix="/ai", tags=["AI Utilities"])
router.include_router(authentication_router, prefix="/auth", tags=["Authentication"])