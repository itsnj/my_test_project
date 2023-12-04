from src.models.order import Order
from fastapi.exceptions import HTTPException

order: dict[int, Order] = {}


def create_order(request: Order):
    if order.get(request.id):
        raise HTTPException(status_code=400, detail="Order Already exists for given id")

    order[request.id] = request
    return "Order Created Successfully"


def update_order(request: dict):
    current_order = order.get(request.get('id'))
    if not current_order:
        raise HTTPException(status_code=400, detail="No order found for the given ID")

    for key, value in request.items():
        setattr(current_order, key, value)

    order[request.get('id')] = current_order
    return "Order Updated Successfully"
