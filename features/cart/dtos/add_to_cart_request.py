from pydantic import BaseModel

from models import OID


class AddToCartRequest(BaseModel):
    productId: OID
