import string
from typing import Union, Optional

from bson import ObjectId
from fastapi import HTTPException

from features.auth.models import CurrentUser
from features.products.dtos import CreateProductRequest
from features.products.models import Product
from models import OID
from utils import mongo_client
import features.jira.jira_service as jira_service

products_collection = mongo_client.products


def get_products(match: dict = None) -> list[Product]:
    product_dicts = products_collection.find(match)

    return [__parse_product(product) for product in product_dicts]


def get_user_products(current_user: CurrentUser, id: string = '') -> list[Product]:
    if id == '':
        return get_products(
        {"ownedBy": jira_service.get_current_jira_user_id(current_user)}
    )
    else:
        return get_products(
        {"ownedBy": id}
    )


def get_products_by_ids(
    product_ids: Optional[list[Union[OID, ObjectId]]]
) -> list[Product]:
    if product_ids is None:
        raise HTTPException(status_code=400, detail="Product ids must be specified.")

    product_dicts = list(products_collection.find({"_id": {"$in": product_ids}}))

    if len(product_dicts) == 0:
        raise HTTPException(status_code=404, detail="No such products found.")

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
        {
            "_id": ObjectId(product_id),
            "ownedBy": jira_service.get_current_jira_user_id(current_user),
        }
    )

    if product is not None:
        raise HTTPException(status_code=400, detail="You may not buy an item twice.")

    product = products_collection.find_one({"_id": ObjectId(product_id)})

    if product["price"] > jira_service.get_my_coins(current_user):
        raise HTTPException(status_code=400, detail="You don't have enough coins.")

    products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$push": {"ownedBy": jira_service.get_current_jira_user_id(current_user)}},
    )


def __parse_product(product: dict) -> Product:
    return Product(
        id=product["_id"],
        name=product["name"],
        description=product["description"],
        image_url=product["image_url"],
        price=product["price"],
    )


def get_price_leaderboard(current_user: CurrentUser) -> list[dict]:
    users = jira_service.get_all_jira_users(current_user)
    leaderboard = []

    for user in users:
        user_products = get_products({"ownedBy": user["accountId"]})
        max_cost = max([p.price for p in user_products]) if len(user_products) else 0
        leaderboard.append(
            {
                "id": user["accountId"],
                "displayName": user["displayName"],
                "mostExpensiveItemCost": max_cost,
            }
        )

    return sorted(leaderboard, key=lambda u: u["mostExpensiveItemCost"], reverse=True)


def get_count_leaderboard(current_user: CurrentUser) -> list[dict]:
    users = jira_service.get_all_jira_users(current_user)
    leaderboard = []

    for user in users:
        user_products = get_products({"ownedBy": user["accountId"]})
        leaderboard.append(
            {
                "id": user["accountId"],
                "displayName": user["displayName"],
                "itemsOwned": len(user_products),
            }
        )

    return sorted(leaderboard, key=lambda u: u["itemsOwned"], reverse=True)
