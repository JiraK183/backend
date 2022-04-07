from datetime import datetime, timedelta
from typing import Optional

from atlassian import Jira
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext

# to get a string like this run:
# openssl rand -hex 32
from requests import HTTPError

from features.auth.dtos import AccessTokenRequest
from utils.env import get_env, JIRA_SPACE, JIRA_USERNAME, JIRA_API_KEY

SECRET_KEY = "dd742d6d03ad786aedf841fcae7f58312fa657331450a887e8b110be962a2de1"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


def get_user(fake_db, username):
    return False


def create_access_token(
    access_token_request: AccessTokenRequest, expires_delta: timedelta
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid JIRA credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        jira = Jira(
            url=access_token_request.space,
            username=access_token_request.username,
            password=access_token_request.api_key,
        )
        jira.get_project("K183")
    except Exception as e:
        print(e)
        raise credentials_exception
    to_encode = access_token_request.dict()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = AccessTokenRequest(username=username)
    except JWTError:
        raise credentials_exception
    # user = get_user(fake_users_db, username=token_data.username)
    # if user is None:
    #     raise credentials_exception
    # return user
