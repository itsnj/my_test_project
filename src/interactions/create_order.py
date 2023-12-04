from src.requests.create_order_request import CreateOrderRequest
from src.repositories.order_repository import create_order
from src.repositories.product_repository import update_product, get_product
from fastapi.exceptions import HTTPException


def create_new_order(request: CreateOrderRequest):
    validate_request(request)
    for i in range(0, len(request.product_ids)):
        blocked_quantity = request.quantity_ordered[i]
        update_product({"blocked_quantity": blocked_quantity})

    return True


def validate_request(request: CreateOrderRequest):
    if len(request.product_ids) != len(request.quantity_ordered):
        raise HTTPException(status_code=400, detail="All the products do not have accurate quantity")
