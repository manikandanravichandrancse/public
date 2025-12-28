from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any
from datetime import datetime


class ProductCreate(BaseModel):
    product_id: str
    name: str
    stock: int
    price: float
    tax_pct: float


class BillItemCreate(BaseModel):
    product_id: str
    quantity: int


class BillCreate(BaseModel):
    customer_email: EmailStr
    items: List[BillItemCreate]
    denominations: Dict[str, int] = {}
    cash_paid: float
