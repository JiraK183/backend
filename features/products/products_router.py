from fastapi import APIRouter, Depends

from features.auth.auth_service import get_current_user
from features.auth.models import CurrentUser
from features.products import products_service
from features.products.dtos import CreateProductRequest
from models import OID

products_router = APIRouter(
    prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)]
)


@products_router.get("/")
async def get_products():
    return {"products": products_service.get_products()}


@products_router.post("/")
async def create_product(create_product_request: CreateProductRequest):
    return products_service.create_product(create_product_request)


@products_router.put("/{product_id}/")
async def update_product(product_id: OID, update_product_request: CreateProductRequest):
    print(product_id)
    print(update_product_request)
    return products_service.update_product(product_id, update_product_request)


@products_router.get("/my")
async def get_my_products(current_user: CurrentUser = Depends(get_current_user)):
    return {"products": products_service.get_user_products(current_user)}


@products_router.delete("/{product_id}/", status_code=204)
async def delete_product(product_id: str):
    products_service.delete_product(product_id)


@products_router.post("/{product_id}/purchase/")
async def purchase_product(
    product_id: str, current_user: CurrentUser = Depends(get_current_user)
):
    return products_service.purchase_product(product_id, current_user)


@products_router.get("/leaderboard/quality")
async def get_leaderboard(current_user: CurrentUser = Depends(get_current_user)):
    return {"leaderboard": products_service.get_price_leaderboard(current_user)}


@products_router.get("/leaderboard/quantity")
async def get_leaderboard(current_user: CurrentUser = Depends(get_current_user)):
    return {"leaderboard": products_service.get_count_leaderboard(current_user)}
