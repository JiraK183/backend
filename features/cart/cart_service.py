from bson import ObjectId
from fastapi import HTTPException

from features.cart.dtos import AddToCartRequest
from features.cart.models import Cart, CartProduct
from features.products import products_service
from utils import redis


max_balance = 100
every_nth_free = 5
discount_from = 20
discount = 1


def get_cart(session_id: str) -> Cart:
    cart_product_quantity = redis.get_from_cache(session_id)

    return _get_cart_with_products(cart_product_quantity)


def add_to_cart(add_to_cart_request: AddToCartRequest, session_id: str):
    add_product_id = str(add_to_cart_request.productId)
    cart_product_quantity = redis.get_from_cache(session_id)

    if cart_product_quantity is None:
        cart_product_quantity = {add_product_id: 1}
    elif add_product_id not in cart_product_quantity:
        cart_product_quantity[add_product_id] = 1
    else:
        cart_product_quantity[add_product_id] += 1

    cart_with_products = _get_cart_with_products(cart_product_quantity)

    if cart_with_products.balance > max_balance:
        raise HTTPException(
            status_code=418,
            detail=f"Cart balance exceeds the ${max_balance} limit.",
        )

    # Cart lasts 30 minutes from latest renewal
    redis.cache(session_id, cart_product_quantity, ex=1800)

    return cart_with_products


def _get_cart_with_products(cart_product_quantity: dict[str, int]) -> Cart:
    product_ids = [ObjectId(product_id) for product_id in cart_product_quantity.keys()]
    products = products_service.get_products_by_ids(product_ids)
    cart_products = [
        CartProduct(
            **product.dict(),
            quantity=cart_product_quantity[str(product.id)],
        )
        for product in products
    ]

    return Cart(
        products=cart_products,
        balance=_get_balance(cart_products),
    )


def _get_balance(cart_products: list[CartProduct]) -> float:
    balance = 0
    for cart_product in cart_products:
        balance += (
            cart_product.price * cart_product.quantity
            - int(cart_product.quantity / every_nth_free) * cart_product.price
        )

    if balance >= discount_from:
        return balance - discount

    return balance
