from src.models.product import Product
from fastapi.exceptions import HTTPException

product: dict[int, Product] = {}


def create_product(request: Product):
    if product.get(request.id):
        raise HTTPException(status_code=400, detail="Product Already exists with given id")

    product[request.id] = request
    return "Product created successfully"


def get_product(product_id: int):
    prod = product.get(product_id)
    if not prod:
        raise HTTPException(status_code=404, detail="No product found")

    return prod.__data__


def update_product(request: dict):
    current_product = product.get(request.get('id'))
    if not current_product:
        raise HTTPException(status_code=404, detail="Requested Product Does no exist")

    for key, value in request.items():
        setattr(current_product, key, value)

    product[current_product.id] = current_product
    return "Product updated successfully"
