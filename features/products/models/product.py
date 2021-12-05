from features.products.enums import ProductType
from models import OID, MongoModel


class Product(MongoModel):
    id: OID
    name: str
    type: ProductType
    price: float
