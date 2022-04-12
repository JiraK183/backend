from fastapi import APIRouter, Depends

from features.statistics import statistics_service

statistics_router = APIRouter(prefix="/statistics", tags=["Statistics"])


@statistics_router.get("/")
async def get_statistics():
    return statistics_service.get_statistics()
