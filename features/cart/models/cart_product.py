from features.products.models import Product


class CartProduct(Product):
    quantity: int = 1
