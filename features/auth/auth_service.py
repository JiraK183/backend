from datetime import datetime, timedelta

from atlassian import Jira
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

from features.auth.dtos import AccessTokenRequest

SECRET_KEY = "dd742d6d03ad786aedf841fcae7f58312fa657331450a887e8b110be962a2de1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
    headers={"WWW-Authenticate": "Bearer"},
)


def create_access_token(access_token_request: AccessTokenRequest):
    __validate_jira(access_token_request)
    to_encode = access_token_request.dict()
    roles = ["user"]
    try:
        jira = Jira(
            url=access_token_request.space,
            username=access_token_request.username,
            password=access_token_request.api_key,
        )
        jira.get_all_permissions()
        roles.append("admin")
    except:
        pass
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "roles": roles})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        access_token_request = AccessTokenRequest(**payload)
        __validate_jira(access_token_request)
    except Exception:
        raise credentials_exception

    return access_token_request


def __validate_jira(access_token_request: AccessTokenRequest) -> None:
    try:
        jira = Jira(
            url=access_token_request.space,
            username=access_token_request.username,
            password=access_token_request.api_key,
        )
        jira.get_project("K183")
    except Exception:
        raise credentials_exception
