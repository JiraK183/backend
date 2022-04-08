from fastapi import APIRouter, Depends

from features.auth.auth_service import get_current_user
from features.auth.models import CurrentUser
from features.coins import coins_service

coins_router = APIRouter(
    prefix="/coins", tags=["Coins"], dependencies=[Depends(get_current_user)]
)


@coins_router.get("/")
async def get_my_coins(current_user: CurrentUser = Depends(get_current_user)):
    return {"coins": coins_service.get_my_coins(current_user)}


@coins_router.get("/leaderboard")
async def get_leaderboard(current_user: CurrentUser = Depends(get_current_user)):
    return {"leaderboard": coins_service.get_leaderboard(current_user)}
