import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from features import (
    coins_router,
    stories_router,
    auth_router,
    statistics_router,
    products_router,
)
from utils.env import get_env, API_PORT

app = FastAPI(docs_url="/")

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(coins_router)
app.include_router(stories_router)
app.include_router(statistics_router)
app.include_router(products_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(get_env(API_PORT)), reload=True)
