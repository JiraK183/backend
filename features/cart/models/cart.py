from features.cart.models import CartProduct
from models import MongoModel


class Cart(MongoModel):
    products: list[CartProduct]
    balance: float
