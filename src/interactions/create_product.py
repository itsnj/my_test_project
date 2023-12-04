from src.models.product import Product
from src.requests.create_product_request import CreateProductRequest
from src.repositories.product_repository import create_product
from fastapi.encoders import jsonable_encoder


def create_new_product(request: CreateProductRequest):
    request = request.model_dump(exclude_none=True)
    try:
        params = Product(**request)
        create_product(params)
    except Exception as e:
        raise e

    return "Product Created"
