from fastapi import APIRouter

from .ai_utilities import router as ai_utilities_router
from .authentication import router as authentication_router

router = APIRouter()

router.include_router(ai_utilities_router, prefix="/ai", tags=["AI Utilities"])
router.include_router(authentication_router, prefix="/auth", tags=["Authentication"])