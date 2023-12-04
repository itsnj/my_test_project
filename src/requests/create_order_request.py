from pydantic import BaseModel


class CreateOrderRequest(BaseModel):
    id: int
    product_ids: list[int]
    quantity_ordered: list[int]
