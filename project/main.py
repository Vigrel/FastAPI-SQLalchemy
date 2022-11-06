from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from core.models import models
from core.models.database import SessionLocal, engine
from core.schemas.schemas import (
    Product,
    ProductCreate,
    ProductGeneral,
    Transaction,
    TransactionCreate,
)
from v1 import crud

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    """
    Uses SessionLocal class to create a dependency. We need to have an independent database
    session/connection (SessionLocal) per request, use the same session through all the
    request and then close it after the request is finished. And then a new session will be
    created for the next request. For that, we will create a new dependency with yield. Our
    dependency will create a new SQLAlchemy SessionLocal that will be used in a single
    request, and then close it once the request is finished.

    Source: https://fastapi.tiangolo.com/tutorial/sql-databases/

    Yields:
        SessionLocal: suspend and retains enough state to maintain db session, until usage
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get(
    "/products/",
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Get all method",
    description="Return all products in database",
)
async def get_products(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Product]:
    """
    Get all method. Return all products in database

    Args:
        skip (int, optional): equivalent to  SQL OFFSET. Defaults to 0.
        limit (int, optional): equivalent to SQL LIMIT. Defaults to 100.
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Returns:
        list[Product]: table of products
    """

    products = crud.get_all_products(db, skip=skip, limit=limit)
    return products


@app.get(
    "/products/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Get method",
    description="Return a specified transaction, by index",
)
async def get_product(product_id: int, db: Session = Depends(get_db)) -> Product:
    """
    Get method. Return a specified transaction, by index

    Args:
        product_id (int): the ID of the product wanted
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error

    Returns:
        Product: a product with all of it's content and it's universal identifier
    """

    product = crud.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


@app.post(
    "/products/",
    response_model=Product,
    status_code=status.HTTP_201_CREATED,
    tags=["Product"],
    summary="Create method",
    description="Create a product based on it's infos and add incremental int id",
)
async def add_product(product: ProductCreate, db: Session = Depends(get_db)) -> Product:
    """
    Create method. Create a product based on it's infos and add incremental int id

    Args:
        product (ProductCreate): a product description (requirements - [name, price])
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the price od the product is less or equal zero, raises 400-BadRequest http error

    Returns:
        Product: a product with all of it's content and it's universal identifier
    """

    if product.price <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't sell it for free"
        )

    return crud.create_product(db=db, product=product)


@app.delete(
    "/products/{product_id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Product"],
    summary="Delete one method",
    description="Delete a product by it's ID",
)
async def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    """
    Delete one method. Delete a product by it's ID

    Args:
        product_id (int): the ID of the product wanted
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error
    """

    product = crud.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    crud.delete_product(db=db, product=product)

    return


@app.patch(
    "/products/{product_id}",
    response_model=Product,
    status_code=status.HTTP_200_OK,
    tags=["Product"],
    summary="Update one method",
    description="Update partialy or intirely a product from db",
)
async def update_item(
    product_id: int,
    modified_product: ProductGeneral,
    db: Session = Depends(get_db),
) -> Product:
    """
    Update one method. Update partialy or intirely a product from db

    Args:
        product_id (int): the ID of the product wanted
        modified_product (ProductGeneral): entity with all new variables to update a product
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error
        HTTPException: if the price od the product is less or equal zero, raises 400-BadRequest http error

    Returns:
        Product: a product with all of it's content and it's universal identifier
    """

    product = crud.get_product(db=db, product_id=product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    if modified_product.price == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Can't sell it for free"
        )

    updated_data = modified_product.dict(exclude_unset=True)
    updated_data["id"] = product_id
    crud.update_product(db=db, product=models.Product(**updated_data))

    return crud.get_product(db=db, product_id=product_id)


@app.post(
    "/transactions/",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
    tags=["Transaction"],
    summary="Create method",
    description="Create a transaction, adding ou removing a quantity of a product",
)
async def buy_sell(
    transaction: TransactionCreate, db: Session = Depends(get_db)
) -> Transaction:
    """
    Create method. Create a transaction, adding ou removing a quantity of a product

    Args:
        transaction (TransactionCreate): _description_
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error
        HTTPException: can't buy or sell 0 products. Raises 400-BadRequest http error
        HTTPException: the sum of the quantity added and the product quantity, must be greater than 0 or will raise 400-BadRequest http error

    Returns:
        Transaction: a transaction with all of it's content and it's universal identifier
    """
    product = crud.get_product(db=db, product_id=transaction.product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    if not transaction.quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Need to add a quantity different than zero",
        )

    if (transaction.quantity + product.quantity) < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough products in inventory",
        )

    product.quantity += transaction.quantity
    crud.update_product(db=db, product=product)

    return crud.create_transaction(db=db, transaction=transaction)


@app.get(
    "/transactions/",
    response_model=list[Product],
    status_code=status.HTTP_200_OK,
    tags=["Transaction"],
    summary="Get all method",
    description="Return all transactions in database",
)
async def get_transactions(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
) -> list[Transaction]:
    """
    Get all method. Return all transactions in database

    Args:
        skip (int, optional): equivalent to  SQL OFFSET. Defaults to 0.
        limit (int, optional): equivalent to SQL LIMIT. Defaults to 100.
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Returns:
        list[Transaction]: table of transactions
    """
    products = crud.get_all_transactions(db, skip=skip, limit=limit)
    return products


@app.get(
    "/transactions/{transaction_id}",
    response_model=Transaction,
    status_code=status.HTTP_200_OK,
    tags=["Transaction"],
    summary="Get method",
    description="Return a specified transaction, by index",
)
async def get_transaction(
    transaction_id: int, db: Session = Depends(get_db)
) -> Transaction:
    """
    Get method. Return a specified transaction, by index

    Args:
        transaction_id (int): the ID of the transaction wanted
        db (Session, optional): databe sesession. Defaults to Depends(get_db).

    Raises:
        HTTPException: if the ID passed isn't in the database, raises 404-NotFound http error

    Returns:
        Transaction: a transaction with all of it's content and it's universal identifier
    """

    transaction = crud.get_transaction(db, transaction_id=transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )

    return transaction
