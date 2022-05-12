from fastapi import APIRouter, Depends
from features.auth.auth_service import get_current_user
from features.auth.models import CurrentUser

from features.statistics import statistics_service

statistics_router = APIRouter(prefix="/statistics", tags=["Statistics"])


@statistics_router.get("/")
async def get_statistics(current_user: CurrentUser = Depends(get_current_user)):
    return statistics_service.get_statistics(current_user)
