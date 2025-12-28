"""API endpoints for billing system."""

import json
import logging
from typing import Dict, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.crud.crud import (
    create_bill,
    create_bill_items,
    create_product,
    get_bill_items,
    get_bills_by_email,
    get_product,
    update_stock,
)
from app.services.billing import BillingService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
logger = logging.getLogger(__name__)


@router.post("/api/products")
async def add_product(
    product_data: dict, db: Session = Depends(get_db)
) -> Dict:
    """
    Add new product with proper error handling.

    Args:
        product_data: Product details
        db: Database session

    Returns:
        Success response with product details
    """
    try:
        # Validate required fields
        required_fields = [
            "product_id",
            "name",
            "stock",
            "price",
            "tax_pct",
        ]
        for field in required_fields:
            if field not in product_data:
                logger.warning(
                    f"Missing field in product creation: {field}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Missing required field: {field}",
                )

        # Validate data types
        if not isinstance(product_data["product_id"], str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="product_id must be string",
            )

        if not isinstance(product_data["stock"], int) or (
            product_data["stock"] < 0
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="stock must be non-negative integer",
            )

        if not isinstance(product_data["price"], (int, float)) or (
            product_data["price"] <= 0
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="price must be positive number",
            )

        if not isinstance(product_data["tax_pct"], (int, float)) or (
            product_data["tax_pct"] < 0
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="tax_pct must be non-negative number",
            )

        # Create product
        product = create_product(db, product_data)
        logger.info(f"Product created: {product.product_id}")

        return {
            "status": "success",
            "message": "Product created successfully",
            "product_id": product.product_id,
            "data": {
                "id": product.id,
                "product_id": product.product_id,
                "name": product.name,
                "stock": product.stock,
                "price": product.price,
                "tax_pct": product.tax_pct,
            },
        }

    except IntegrityError as e:
        db.rollback()
        logger.error(f"Duplicate product: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Product ID already exists",
        ) from e

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        ) from e

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e


@router.get("/")
async def billing_page(request: Request):
    """Billing page (Page 1)."""
    logger.info("Billing page accessed")
    return templates.TemplateResponse("page1.html", {"request": request})


@router.post("/api/generate-bill")
async def generate_bill(
    request: Request,
    customer_email: str = Form(...),
    items_json: str = Form(...),
    cash_paid: float = Form(...),
    db: Session = Depends(get_db),
) -> JSONResponse:
    """
    Generate bill and save to database.

    Args:
        request: HTTP request
        customer_email: Customer email
        items_json: JSON string of bill items
        cash_paid: Cash paid by customer
        db: Database session

    Returns:
        Bill confirmation page or error
    """
    try:
        # Validate email
        if not customer_email or "@" not in customer_email:
            logger.warning(f"Invalid email format: {customer_email}")
            return templates.TemplateResponse(
                "page1.html",
                {
                    "request": request,
                    "error": "Invalid email address",
                },
            )

        # Parse items
        try:
            items = json.loads(items_json)
        except json.JSONDecodeError:
            logger.error("Invalid items JSON format")
            return templates.TemplateResponse(
                "page1.html",
                {"request": request, "error": "Invalid items format"},
            )

        if not items or len(items) == 0:
            logger.warning("No items in bill")
            return templates.TemplateResponse(
                "page1.html",
                {"request": request, "error": "No items in bill"},
            )

        if cash_paid <= 0:
            logger.warning("Invalid cash amount")
            return templates.TemplateResponse(
                "page1.html",
                {
                    "request": request,
                    "error": "Cash paid must be positive",
                },
            )

        # Validate and fetch products
        products = {}
        for item in items:
            if "product_id" not in item or "quantity" not in item:
                logger.error("Invalid item format")
                return templates.TemplateResponse(
                    "page1.html",
                    {"request": request, "error": "Invalid item format"},
                )

            product = get_product(db, item["product_id"])
            if not product:
                logger.warning(f"Product not found: {item['product_id']}")
                return templates.TemplateResponse(
                    "page1.html",
                    {
                        "request": request,
                        "error": (
                            f"Product {item['product_id']} not found"
                        ),
                    },
                )

            if product.stock < item["quantity"]:
                logger.warning(
                    f"Insufficient stock for {item['product_id']}"
                )
                return templates.TemplateResponse(
                    "page1.html",
                    {
                        "request": request,
                        "error": (
                            f"Insufficient stock for {item['product_id']}. "
                            f"Available: {product.stock}"
                        ),
                    },
                )

            products[item["product_id"]] = {
                "price": float(product.price),
                "tax_pct": float(product.tax_pct),
            }

        # Calculate bill
        bill_service = BillingService()
        bill_calc = bill_service.calculate(items, products)
        bill_calc["cash_paid"] = cash_paid
        bill_calc["change_due"] = cash_paid - bill_calc["rounded_total"]

        # Validate payment
        if bill_calc["change_due"] < 0:
            logger.warning(
                f"Insufficient payment: {cash_paid} < "
                f"{bill_calc['rounded_total']}"
            )
            return templates.TemplateResponse(
                "page1.html",
                {
                    "request": request,
                    "error": (
                        f"Insufficient payment. Need "
                        f"Rs.{bill_calc['rounded_total']}, "
                        f"got Rs.{cash_paid}"
                    ),
                },
            )

        # Calculate denominations
        balance_denoms = bill_service.calculate_change(
            bill_calc["change_due"]
        )

        # Update stock and save bill
        for item in items:
            if not update_stock(
                db, item["product_id"], item["quantity"]
            ):
                db.rollback()
                logger.error(
                    f"Failed to update stock for {item['product_id']}"
                )
                return templates.TemplateResponse(
                    "page1.html",
                    {
                        "request": request,
                        "error": (
                            f"Failed to update stock for "
                            f"{item['product_id']}"
                        ),
                    },
                )

        # Save bill
        bill_data = {
            "customer_email": customer_email,
            "total_pre_tax": bill_calc["total_pre_tax"],
            "total_tax": bill_calc["total_tax"],
            "net_total": bill_calc["net_total"],
            "rounded_total": bill_calc["rounded_total"],
            "cash_paid": cash_paid,
            "change_due": bill_calc["change_due"],
            "balance_denominations": json.dumps(balance_denoms),
        }
        bill = create_bill(db, bill_data)
        create_bill_items(db, bill.id, bill_calc["items"])

        logger.info(
            f"Bill generated for {customer_email}: "
            f"Rs.{bill_calc['rounded_total']}"
        )

        # Render response
        return templates.TemplateResponse(
            "page2.html",
            {
                "request": request,
                "bill": bill,
                "items": bill_calc["items"],
                "total_pre_tax": bill_calc["total_pre_tax"],
                "total_tax": bill_calc["total_tax"],
                "net_total": bill_calc["net_total"],
                "rounded_total": bill_calc["rounded_total"],
                "cash_paid": cash_paid,
                "change_due": bill_calc["change_due"],
                "balance_denoms": balance_denoms,
                "customer_email": customer_email,
            },
        )

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        return templates.TemplateResponse(
            "page1.html",
            {"request": request, "error": "Database error occurred"},
        )

    except Exception as e:
        db.rollback()
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        return templates.TemplateResponse(
            "page1.html", {"request": request, "error": f"Error: {str(e)}"}
        )


@router.get("/history")
async def history_page(request: Request):
    """Bill history page."""
    logger.info("History page accessed")
    return templates.TemplateResponse("history.html", {"request": request})


@router.get("/api/bills/{email}")
async def get_bills(
    email: str, db: Session = Depends(get_db)
) -> Dict:
    """
    Get bills by email.

    Args:
        email: Customer email address
        db: Database session

    Returns:
        List of bills for the customer
    """
    try:
        if not email or "@" not in email:
            logger.warning(f"Invalid email format: {email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format",
            )

        bills = get_bills_by_email(db, email)
        result = [
            {
                "id": bill.id,
                "customer_email": bill.customer_email,
                "rounded_total": bill.rounded_total,
                "created_at": (
                    bill.created_at.isoformat()
                    if bill.created_at
                    else None
                ),
            }
            for bill in bills
        ]

        logger.info(f"Retrieved {len(result)} bills for {email}")

        return {
            "status": "success",
            "count": len(result),
            "bills": result,
        }

    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred",
        ) from e

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        ) from e
