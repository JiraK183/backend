from features.cart.dtos import AddToCartRequest
from features.cart.models.cart import Cart
from utils import redis


# TODO: implement get_cart
def get_cart(session_id: str) -> Cart:
    pass

    # cart_dict = redis.get_from_cache(session_id)
    #
    # return _get_cart(cart_dict)


# TODO: implement add_to_cart
def add_to_cart(add_to_cart_request: AddToCartRequest, session_id: str):
    redis.cache(session_id, add_to_cart_request, ex=30)

    return _get_cart({})


def _get_cart(cart: dict) -> Cart:
    # TODO: calculate balance, get products

    return Cart(products=[], balance=0)
