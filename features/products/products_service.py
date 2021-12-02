from bson import ObjectId
from fastapi import HTTPException

from features.products.dtos import CreateProductRequest
from features.products.enums import ProductType
from features.products.models import Product
from models import OID
from utils import mongo_client

products_collection = mongo_client.products


def get_products() -> list[Product]:
    product_dicts = products_collection.find()

    return [_parse_product(product) for product in product_dicts]


def get_products_by_ids(product_ids: list[OID]) -> list[Product]:
    product_dicts = list(products_collection.find({"_id": {"$in": product_ids}}))

    if len(product_dicts) == 0:
        raise HTTPException(status_code=404, detail="No such products not found.")

    return [_parse_product(product) for product in product_dicts]


def create_product(
    create_product_request: CreateProductRequest,
) -> Product:
    request_body = create_product_request.dict()

    # OpenAPI 'type' enum matching (instead of str)
    _id = products_collection.insert_one(
        {**request_body, "type": request_body["type"].value}
    )

    return Product(
        **request_body,
        id=str(_id.inserted_id),
    )


def delete_product(product_id: str) -> None:
    result = products_collection.delete_one({"_id": ObjectId(product_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Product not found.")


def _parse_product(product: dict) -> Product:
    return Product(
        id=str(product["_id"]),
        name=product["name"],
        type=ProductType(product["type"]),
        price=product["price"],
        quantity=product["quantity"],
    )
