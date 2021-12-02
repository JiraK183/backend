from fastapi import APIRouter

from features.cart import cart_service
from features.cart.dtos import AddToCartRequest

cart_router = APIRouter(prefix="/cart", tags=["Cart"])

session_id_from_header = "demo_session_idx"


@cart_router.get("/")
async def get_cart(session_id: str = session_id_from_header):
    return cart_service.get_cart(session_id)


@cart_router.post("/")
async def add_to_cart(
    add_to_cart_request: AddToCartRequest, session_id: str = session_id_from_header
):
    return cart_service.add_to_cart(add_to_cart_request, session_id)
