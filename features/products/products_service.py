from typing import Union, Optional

from bson import ObjectId
from fastapi import HTTPException

from features.auth.models import CurrentUser
from features.products.dtos import CreateProductRequest
from features.products.models import Product
from models import OID
from utils import mongo_client

products_collection = mongo_client.products


def get_products(match: dict = None) -> list[Product]:
    product_dicts = products_collection.find(match)

    return [__parse_product(product) for product in product_dicts]


def get_user_products(current_user: CurrentUser) -> list[Product]:
    return get_products({"ownedBy": current_user.username})


def get_products_by_ids(
    product_ids: Optional[list[Union[OID, ObjectId]]]
) -> list[Product]:
    if product_ids is None:
        raise HTTPException(status_code=400, detail="Product ids must be specified.")

    product_dicts = list(products_collection.find({"_id": {"$in": product_ids}}))

    if len(product_dicts) == 0:
        raise HTTPException(status_code=404, detail="No such products not found.")

    return [__parse_product(product) for product in product_dicts]


def create_product(
    create_product_request: CreateProductRequest,
) -> Product:
    request_body = create_product_request.dict()

    # OpenAPI 'type' enum matching (instead of str)
    _id = products_collection.insert_one(request_body)

    return Product(
        **request_body,
        id=_id.inserted_id,
    )


def delete_product(product_id: str) -> None:
    result = products_collection.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found.")


def purchase_product(product_id: str, current_user: CurrentUser) -> None:
    get_products_by_ids([ObjectId(product_id)])  # 404 not found validation

    product = products_collection.find_one(
        {"_id": ObjectId(product_id), "ownedBy": current_user.username}
    )

    if product is not None:
        raise HTTPException(status_code=400, detail="You may not buy an item twice.")

    products_collection.update_one(
        {"_id": ObjectId(product_id)}, {"$push": {"ownedBy": current_user.username}}
    )


def __parse_product(product: dict) -> Product:
    return Product(
        id=product["_id"],
        name=product["name"],
        description=product["description"],
        image_url=product["image_url"],
        price=product["price"],
    )
