from pydantic import BaseModel


class ProductGeneral(BaseModel):
    name: str | None = None
    price: float | None = None
    tax: float | None = None
    description: str | None = None


class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int = 0


class ProductCreate(ProductBase):
    tax: float | None = None
    description: str | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "price": 35.4,
                "tax": 3.2,
                "description": "A very nice product",
            }
        }


class Product(ProductBase):
    id: int
    tax: float | None = None
    description: str | None = None

    class Config:
        orm_mode = True


class TransactionBase(BaseModel):
    product_id: int
    quantity: int


class TransactionCreate(TransactionBase):
    class Config:
        schema_extra = {
            "example": {
                "product_id": 42,
                "quantity": 21,
            }
        }


class Transaction(TransactionBase):
    id: int

    class Config:
        orm_mode = True
