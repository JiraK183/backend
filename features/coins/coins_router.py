from fastapi import APIRouter

from features.coins import coins_service

coins_router = APIRouter(prefix="/coins", tags=["Coins"])


@coins_router.get("/")
async def get_my_coins():
    return {"coins": coins_service.get_my_coins()}


@coins_router.get("/leaderboard")
async def get_leaderboard():
    return {"leaderboard": coins_service.get_leaderboard()}
