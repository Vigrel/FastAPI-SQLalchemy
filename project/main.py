from uuid import uuid4

from fastapi import FastAPI, HTTPException, status
from core.schemas.Product import ProductDB, ProductGeneral, ProductPost
from core.models.db import products


app = FastAPI()


@app.get(
    "/products/",
    response_model=list[ProductDB],
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Get all method",
    description="Return all products in database",
)
async def get_products() -> list[ProductDB]:
    """
    get_all method. Return all products in database

    Returns:
        list[ProductDB]: database
    """
    return products


@app.delete(
    "/products/{product_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Product"],
    summary="Delete one method",
    description="Delete a product by it's ID",
)
async def delete_product(product_id: str) -> dict[str]:
    """
    delete_one method. Delete a product by it's ID

    Args:
        product_id (str): a version 4 universally unique identifier

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error

    Returns:
        dict[str]: simple message identifying the product deletion
    """
    for product in products:
        if product.id == product_id:
            products.remove(product)
            return {"message": "resource deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )


@app.post(
    "/products/",
    response_model=ProductDB,
    status_code=status.HTTP_201_CREATED,
    tags=["Product"],
    summary="Create method",
    description="Create a product based on it's infos and add a random uuid4 id",
)
async def add_product(product: ProductPost) -> ProductDB:
    """
    post method. Create a product based on it's infos and add a random id.

    Args:
        product (ProductPost): a product description (requirements - [quantity, name, price])

    Returns:
        ProductDB: a product with all of it's content and it's universal identifier
    """
    product_dict = product.dict()
    product_dict["id"] = str(uuid4())
    products.append(ProductDB(**product_dict))
    return products[-1]


@app.patch(
    "/products/{product_id}",
    response_model=ProductDB,
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Update one method",
    description="Update partialy or intirely a product from db",
)
async def update_item(product_id: str, modified_product: ProductGeneral) -> ProductDB:
    """
    update_one method. Allows user to modify every variavle in a Product from the DB (can't edit ID)

    Args:
        product_id (str):  a version 4 universally unique identifier
        modified_product (ProductGeneral): entity with all new variables to update a product

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error

    Returns:
        ProductDB: a product with all of it's content and it's universal identifier
    """
    for product in products:
        if product.id == product_id:
            update_data = modified_product.dict(exclude_unset=True)
            update_data["id"] = product_id
            updated_product = product.copy(update=update_data)
            products[products.index(product)] = updated_product
            return updated_product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
    )
