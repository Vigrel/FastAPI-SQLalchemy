from pydantic import BaseModel


class ProductGeneral(BaseModel):
    quantity: int | None = None
    name: str | None = None
    price: float | None = None
    tax: float | None = None
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "quantity": "100",
                "name": "Foo",
                "price": 35.4,
                "tax": 3.2,
                "description": "A very nice product",
            }
        }


class ProductDB(ProductGeneral):
    id: str
    quantity: int
    name: str
    price: float


class ProductPost(ProductGeneral):
    quantity: int
    name: str
    price: float
