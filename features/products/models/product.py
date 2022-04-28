from models import OID, MongoModel


class Product(MongoModel):
    id: OID
    name: str
    description: str
    image_url: str
    price: float

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.description == other.description
            and self.image_url == other.image_url
            and self.price == other.price
        )
