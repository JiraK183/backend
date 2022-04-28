from fastapi import APIRouter, Depends

from features.auth.auth_service import get_current_user
from features.products import products_service
from features.products.dtos import CreateProductRequest

products_router = APIRouter(
    prefix="/products", tags=["Products"], dependencies=[Depends(get_current_user)]
)


@products_router.get("/")
async def get_products():
    return {"products": products_service.get_products()}


# @products_router.get("/ids")
# async def get_products_by_ids(product_ids: list[OID] = Query(None)):
#     return {"products": products_service.get_products_by_ids(product_ids)}


@products_router.post("/")
async def create_product(create_product_request: CreateProductRequest):
    return products_service.create_product(create_product_request)


@products_router.delete("/{product_id}/", status_code=204)
async def delete_product(product_id: str):
    products_service.delete_product(product_id)
