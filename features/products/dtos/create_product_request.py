from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    name: str
    description: str
    image_url: str
    price: int
