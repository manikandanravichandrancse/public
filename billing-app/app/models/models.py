"""SQLAlchemy ORM models for database tables."""

from datetime import datetime
from uuid import uuid4

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    """Product model for inventory management."""

    __tablename__ = "products"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    product_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    stock = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    tax_pct = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation of Product."""
        return f"<Product {self.product_id}: {self.name}>"


class Bill(Base):
    """Bill model for transaction records."""

    __tablename__ = "bills"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    customer_email = Column(String, nullable=False)
    total_pre_tax = Column(Float, nullable=False)
    total_tax = Column(Float, nullable=False)
    net_total = Column(Float, nullable=False)
    rounded_total = Column(Float, nullable=False)
    cash_paid = Column(Float, nullable=False)
    change_due = Column(Float, nullable=False)
    balance_denominations = Column(String)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation of Bill."""
        return f"<Bill {self.id[:8]}: {self.customer_email}>"


class BillItem(Base):
    """BillItem model for individual items in a bill."""

    __tablename__ = "bill_items"

    id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    bill_id = Column(String, ForeignKey("bills.id"), nullable=False)
    product_id = Column(String, nullable=False)
    unit_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    tax_pct = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        """String representation of BillItem."""
        return f"<BillItem {self.product_id}: Qty={self.quantity}>"
