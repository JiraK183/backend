from fastapi import APIRouter, Depends

from features.auth.auth_service import get_current_user
from features.auth.models import CurrentUser
from features.stories import stories_service

stories_router = APIRouter(
    prefix="/stories", tags=["Stories"], dependencies=[Depends(get_current_user)]
)


@stories_router.get("/active")
async def get_active_stories(current_user: CurrentUser = Depends(get_current_user)):
    return {"stories": stories_service.get_active_stories(current_user)}


@stories_router.get("/completed-today")
async def get_completed_today_stories(
    current_user: CurrentUser = Depends(get_current_user),
):
    return {"stories": stories_service.get_completed_today_stories(current_user)}
