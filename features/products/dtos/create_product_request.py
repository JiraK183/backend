from pydantic import BaseModel

from features.products.enums import ProductType


class CreateProductRequest(BaseModel):
    name: str
    type: ProductType
    price: float
