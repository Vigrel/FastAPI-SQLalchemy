from fastapi import FastAPI, Path, HTTPException
from enum import Enum
from pydantic import BaseModel
from models import *
import itertools

counter = itertools.count()


products = [
    Product(id=next(counter), name="Product 1", description="Description 1", price=10.0, quantity=10, tax=0.5),
]
app = FastAPI()


@app.get("/products/", response_model=list[Product])
async def get_products():
    return products

@app.delete("/products/{product_id}", status_code=204, response_model=None)
async def get_product(product_id: int = Path(..., title="The ID of the item to delete")):
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return
    raise HTTPException(status_code=404, detail="Product not found")
    


@app.post("/products/", status_code=201)
async def add_product(product: Product, response_model=Product):
    product.id = next(counter)
    product_dict = product.dict()
    # if product.name in products:
    #     raise HTTPException(status_code=400, detail="Product already exists")
    products.append(Product(**product_dict))
    return product


