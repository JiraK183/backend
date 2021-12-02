import uvicorn
from fastapi import FastAPI

from features import products_router, cart_router

app = FastAPI(docs_url="/")

app.include_router(products_router)
app.include_router(cart_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
