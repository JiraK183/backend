from fastapi import APIRouter

from features.coins import coins_service

coins_router = APIRouter(prefix="/coins", tags=["Coins"])


@coins_router.get("/")
async def get_my_coins():
    return {"coins": coins_service.get_my_coins()}


@coins_router.get("/leaderboard")
async def get_leaderboard():
    return {"leaderboard": coins_service.get_leaderboard()}


@coins_router.get("/active")
async def get_active_stories(current_user: str):
    return {"stories": coins_service.get_active(current_user)}


@coins_router.get("/completed-today")
async def get_completed_today_stories(current_user: str):
    return {"stories": coins_service.get_completed_today_stories(current_user)}
