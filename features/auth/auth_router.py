from fastapi import APIRouter

# to get a string like this run:
# openssl rand -hex 32
from features.auth import auth_service
from features.auth.dtos import AccessTokenRequest, AccessTokenResponse


auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/token", response_model=AccessTokenResponse)
async def get_access_token(access_token_request: AccessTokenRequest):
    access_token = auth_service.create_access_token(
        access_token_request=access_token_request
    )

    return {
        "access_token": f"Bearer {access_token}",
    }
