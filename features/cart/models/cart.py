from pydantic import BaseModel

from features.products.models import Product


class Cart(BaseModel):
    products: list[Product]
    balance: float
