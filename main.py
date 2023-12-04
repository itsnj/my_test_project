from fastapi import FastAPI
from src.router import my_route
from src.interactions.create_product import create_new_product
from src.interactions.get_product_detail import get_product_detail
from src.requests.create_product_request import CreateProductRequest


print(create_new_product(CreateProductRequest(**{"id": 1, "name": "Prod1", "count": 10, "blocked_count": 0})))
print(create_new_product(CreateProductRequest(**{"id": 2, "name": "Prod2", "count": 9, "blocked_count": 0})))
print(get_product_detail(1))
print(get_product_detail(2))

docs = {
    "title": "My Project",
    "docs_url": "/project/docs",
    "redoc_url": "/project/redoc",
    "openapi_url": "/project/openapi.json",
    "debug": True,
    "swagger_ui_parameters": {"docExpansion": None},
}

app = FastAPI(**docs)


app.include_router(
    prefix="/project",
    router=my_route,
    tags=["Product route"]
)
