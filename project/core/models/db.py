from uuid import uuid4

from core.schemas.Product import ProductDB

products = [
    ProductDB(
        id=str(uuid4()),
        name="Bananas",
        description="A product loved by minions",
        price=10.0,
        quantity=10000,
    ),
    ProductDB(
        id=str(uuid4()),
        name="RTX 3090",
        description="A product loved by gamers",
        price=1000.0,
        quantity=1,
        tax=50.0,
    ),
    ProductDB(
        id=str(uuid4()),
        name="Bike wheel",
        description="A product loved by triathlete",
        price=100.0,
        quantity=555,
        tax=25.0,
    ),
]
