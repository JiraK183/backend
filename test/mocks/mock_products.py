from bson import ObjectId

from features.products.enums import ProductType
from features.products.models import Product

coke = Product(
    id=ObjectId("6003866ba37b1acb2d7d7056"),
    name="Coca-Cola",
    type=ProductType.COKE,
    price=1.19,
)

coke_zero = Product(
    id=ObjectId("6003866ba37b1acb2d7d7057"),
    name="Coca-Cola Zero",
    type=ProductType.COKE,
    price=0.99,
)

crystal_pepsi = Product(
    id=ObjectId("6003866ba37b1acb2d7d7058"),
    name="Crystal Pepsi",
    type=ProductType.PEPSI,
    price=24.50,
)

sprite = Product(
    id=ObjectId("6003866ba37b1acb2d7d7059"),
    name="Sprite",
    type=ProductType.SPRITE,
    price=0.95,
)


fanta = Product(
    id=ObjectId("6003866ba37b1acb2d7d7060"),
    name="Fanta",
    type=ProductType.FANTA,
    price=0.70,
)
