# For the sake of simplicity, there won't be a separate mongo or redis instance

from pymongo import MongoClient

from features.products.models import Product
from tests.mocks import mock_products
from utils import redis_client


def get_product_dict(product: Product):
    return {**product.dict(), "_id": product.id, "type": product.type.value}


def create_mock_data(mongo_client: MongoClient):
    database_products = mongo_client.products

    database_products.drop()
    redis_client.flushdb()

    database_products.insert_one(get_product_dict(mock_products.coke))
    database_products.insert_one(get_product_dict(mock_products.coke_zero))
    database_products.insert_one(get_product_dict(mock_products.crystal_pepsi))
    database_products.insert_one(get_product_dict(mock_products.sprite))
