from src.models.product import Product
from src.repositories.product_repository import get_product


def get_product_detail(product_id: int):
    prod = get_product(product_id)
    if prod:
        return prod

    return "Product Not found"
