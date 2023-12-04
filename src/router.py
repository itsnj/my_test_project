from fastapi import APIRouter
from src.interactions.create_product import create_new_product
from src.interactions.get_product_detail import get_product_detail
from src.requests.create_product_request import CreateProductRequest
from src.requests.create_order_request import CreateOrderRequest
from src.interactions.create_order import create_new_order

my_route = APIRouter()


@my_route.get("/get_api")
def get_api(product_id: int):
    return get_product_detail(product_id)


@my_route.post("/create_product")
def create_product_api(request: CreateProductRequest):
    try:
        response = create_new_product(request)
    except Exception as e:
        raise e

    return response


@my_route.post("/create_order")
def create_order_api(request: CreateOrderRequest):
    try:
        response = create_new_order(request)
    except Exception as e:
        raise e

    return response
