import uvicorn
from fastapi import FastAPI

from features import products_router
from utils.env import get_env, API_PORT

app = FastAPI(docs_url="/")

app.include_router(products_router)

# test

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(get_env(API_PORT)), reload=True)
