from pydantic import BaseModel

class Product(BaseModel):
    id: int | None = None
    name: str
    description: str | None = None
    price: float
    quantity: int