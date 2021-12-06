from features.products.enums import ProductType
from models import OID, MongoModel


class Product(MongoModel):
    id: OID
    name: str
    type: ProductType
    price: float

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.type == other.type
            and self.price == other.price
        )
