from core.models.database import Base
from sqlalchemy import Column, Float, ForeignKey, Integer, String


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(50), index=True, nullable=False)
    price = Column(Float, index=True, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax = Column(Float, index=True)
    description = Column(String(200), index=True)


class Transaction(Base):
    __tablename__ = "transaction"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, index=True, nullable=False)
