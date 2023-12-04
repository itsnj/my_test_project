from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    id: int
    name: str
    count: int
    blocked_count: int = 0
