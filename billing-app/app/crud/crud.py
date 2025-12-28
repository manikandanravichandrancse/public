"""CRUD operations for database models."""

from typing import Dict, List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.models import Bill, BillItem, Product


def get_product(db: Session, product_id: str) -> Optional[Product]:
    """
    Get product by product_id.

    Args:
        db: Database session
        product_id: Product identifier

    Returns:
        Product object or None if not found
    """
    return db.scalar(select(Product).where(Product.product_id == product_id))


def update_stock(db: Session, product_id: str, quantity: int) -> bool:
    """
    Update product stock after purchase.

    Args:
        db: Database session
        product_id: Product identifier
        quantity: Quantity to decrease

    Returns:
        True if update successful, False if insufficient stock
    """
    product = get_product(db, product_id)
    if product and product.stock >= quantity:
        product.stock -= quantity
        db.commit()
        db.refresh(product)
        return True
    return False


def create_product(db: Session, product_data: dict) -> Product:
    """
    Create a new product.

    Args:
        db: Database session
        product_data: Dictionary with product information

    Returns:
        Created Product object
    """
    product = Product(**product_data)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def create_bill(db: Session, bill_data: dict) -> Bill:
    """
    Create a new bill.

    Args:
        db: Database session
        bill_data: Dictionary with bill information

    Returns:
        Created Bill object
    """
    bill = Bill(**bill_data)
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def create_bill_items(db: Session, bill_id: str, items: List[Dict]) -> None:
    """
    Create bill items for a bill.

    Args:
        db: Database session
        bill_id: Bill identifier
        items: List of item dictionaries
    """
    for item in items:
        item_with_bill = {
            "bill_id": bill_id,
            "product_id": item.get("product_id"),
            "unit_price": item.get("unit_price"),
            "quantity": item.get("quantity"),
            "tax_pct": item.get("tax_pct"),
            "subtotal": item.get("subtotal"),
        }
        db_item = BillItem(**item_with_bill)
        db.add(db_item)
    db.commit()


def get_bills_by_email(db: Session, email: str) -> List[Bill]:
    """
    Get all bills for a customer email.

    Args:
        db: Database session
        email: Customer email address

    Returns:
        List of Bill objects ordered by creation date (newest first)
    """
    return db.scalars(
        select(Bill)
        .where(Bill.customer_email == email)
        .order_by(Bill.created_at.desc())
    ).all()


def get_bill_items(db: Session, bill_id: str) -> List[BillItem]:
    """
    Get all items for a specific bill.

    Args:
        db: Database session
        bill_id: Bill identifier

    Returns:
        List of BillItem objects ordered by creation date
    """
    return db.scalars(
        select(BillItem)
        .where(BillItem.bill_id == bill_id)
        .order_by(BillItem.created_at)
    ).all()
