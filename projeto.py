from fastapi import FastAPI, Path, HTTPException
from enum import Enum
from pydantic import BaseModel
from models import *

products = [
    Product(id=0, name="Product 1", description="Description 1", price=10.0, quantity=10, tax=0.5),
]
app = FastAPI()


@app.get("/products/", response_model=list[Product])
async def get_products():
    return products

# @app.get("/products/{product_id}")
# async def get_product(product_id: int = Path(..., gt=0, le=len(products))):

@app.post("/products/", status_code=201)
async def add_product(product: Product):
    product_dict = product.dict()
    if product.name in products:
        raise HTTPException(status_code=400, detail="Product already exists")
    product_dict["id"] = len(products)
    products.append(Product(**product_dict))
    return product


