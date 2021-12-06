import unittest

from fastapi import HTTPException

from features.products import products_service
from features.products.dtos import CreateProductRequest
from tests.mocks import mock_products
from tests.setup import create_mock_data
from utils import mongo_client


class TestProductsService(unittest.TestCase):
    def setUp(self):
        create_mock_data(mongo_client)

    def test_get_products(self):
        products = products_service.get_products()

        self.assertEqual(
            4,
            len(products),
        )
        self.assertEqual(
            [
                mock_products.coke,
                mock_products.coke_zero,
                mock_products.crystal_pepsi,
                mock_products.sprite,
            ],
            products,
        )

    def test_create_product(self):
        inserted_fanta = products_service.create_product(
            create_product_request=CreateProductRequest(**mock_products.fanta.dict())
        )

        self.assertEqual(
            mock_products.fanta,
            inserted_fanta,
        )

    def test_delete_product(self):
        inserted_fanta = products_service.create_product(
            create_product_request=CreateProductRequest(**mock_products.fanta.dict())
        )

        products_service.delete_product(product_id=inserted_fanta.id)

        self.assertRaises(
            HTTPException,
            products_service.get_products_by_ids,
            [inserted_fanta.id],
        )


if __name__ == "__main__":
    unittest.main()
