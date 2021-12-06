import unittest

from fastapi import HTTPException

from features.cart import cart_service
from features.cart.dtos import AddToCartRequest
from features.cart.models import CartProduct, Cart
from tests.mocks import mock_products
from tests.setup import create_mock_data
from utils import mongo_client


test_session_id = "it_test"


class TestCartService(unittest.TestCase):
    def setUp(self):
        create_mock_data(mongo_client)

    def test_add_to_cart(self):
        cart = cart_service.add_to_cart(
            add_to_cart_request=AddToCartRequest(
                productId=mock_products.sprite.id,
            ),
            session_id=test_session_id,
        )

        self.assertEqual(
            Cart(
                products=[CartProduct(**mock_products.sprite.dict(), quantity=1)],
                balance=0.95,
            ),
            cart,
        )

    def test_discount(self):
        cart_service.add_to_cart(
            add_to_cart_request=AddToCartRequest(
                productId=mock_products.crystal_pepsi.id,
            ),
            session_id=test_session_id,
        )

        cart = cart_service.get_cart(test_session_id)

        self.assertEqual(
            Cart(
                products=[
                    CartProduct(**mock_products.crystal_pepsi.dict(), quantity=1)
                ],
                balance=23.5,
            ),
            cart,
        )

    def test_nth_free(self):
        for i in range(0, 10):
            cart_service.add_to_cart(
                add_to_cart_request=AddToCartRequest(
                    productId=mock_products.coke.id,
                ),
                session_id=test_session_id,
            )

        cart = cart_service.get_cart(test_session_id)

        self.assertEqual(
            Cart(
                products=[CartProduct(**mock_products.coke.dict(), quantity=10)],
                balance=9.52,
            ),
            cart,
        )

    def test_exceeds_balance(self):
        for i in range(0, 5):
            cart_service.add_to_cart(
                add_to_cart_request=AddToCartRequest(
                    productId=mock_products.crystal_pepsi.id,
                ),
                session_id=test_session_id,
            )

        cart = cart_service.get_cart(test_session_id)

        self.assertEqual(
            Cart(
                products=[
                    CartProduct(**mock_products.crystal_pepsi.dict(), quantity=5)
                ],
                balance=97.0,
            ),
            cart,
        )
        self.assertRaises(
            HTTPException,
            cart_service.add_to_cart,
            AddToCartRequest(
                productId=mock_products.crystal_pepsi.id,
            ),
            test_session_id,
        )


if __name__ == "__main__":
    unittest.main()
