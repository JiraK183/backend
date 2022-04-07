from fastapi import APIRouter

from features.stories import stories_service

stories_router = APIRouter(prefix="/stories", tags=["Stories"])


@stories_router.get("/active")
async def get_active_stories(current_user: str):
    return {"stories": stories_service.get_active_stories(current_user)}


@stories_router.get("/completed-today")
async def get_completed_today_stories(current_user: str):
    return {"stories": stories_service.get_completed_today_stories(current_user)}
