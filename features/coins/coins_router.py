from fastapi import APIRouter

from features.coins import coins_service

coins_router = APIRouter(prefix="/coins", tags=["Coins"])


@coins_router.get("/")
async def get_my_coins():
    return {"coins": coins_service.get_my_coins()}


@coins_router.get("/leaderboard")
async def get_leaderboard():
    return {"leaderboard": coins_service.get_leaderboard()}


@coins_router.get("/my-active-stories")
async def get_my_active_stories(userName: str):
    return {"my_active_stories": coins_service.get_my_active_stories(userName)}


@coins_router.get("/my-completed-stories-today")
async def get_my_completed_stories_today(userName: str):
    return {
        "my_completed_stories_today": coins_service.get_my_completed_stories_today(
            userName
        )
    }
