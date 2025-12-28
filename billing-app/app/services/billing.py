"""Billing calculation service."""

from typing import Dict, List


class BillingService:
    """Service for calculating bills and denominations."""

    def calculate(self, items: List[Dict], products: Dict) -> Dict:
        """
        Calculate bill with tax and rounding.

        Args:
            items: List of items with product_id and quantity
            products: Dict of product details with price and tax_pct

        Returns:
            Dict with calculated bill details
        """
        total_pre_tax = 0.0
        total_tax = 0.0
        bill_items = []

        for item in items:
            product_id = item["product_id"]
            quantity = item["quantity"]
            product = products[product_id]
            unit_price = product["price"]
            tax_pct = product["tax_pct"]

            # Calculate per item
            item_pre_tax = unit_price * quantity
            item_tax = item_pre_tax * (tax_pct / 100)
            item_total = item_pre_tax + item_tax

            total_pre_tax += item_pre_tax
            total_tax += item_tax

            bill_items.append(
                {
                    "product_id": product_id,
                    "unit_price": unit_price,
                    "quantity": quantity,
                    "tax_pct": tax_pct,
                    "subtotal": item_total,
                }
            )

        net_total = total_pre_tax + total_tax
        rounded_total = int(net_total)  # Rounds down to nearest integer

        return {
            "items": bill_items,
            "total_pre_tax": round(total_pre_tax, 2),
            "total_tax": round(total_tax, 2),
            "net_total": round(net_total, 2),
            "rounded_total": rounded_total,
        }

    def calculate_change(self, amount: float) -> Dict[int, int]:
        """
        Calculate denomination breakdown for change.

        Args:
            amount: Total change amount in rupees

        Returns:
            Dict with denominations as keys and counts as values
        """
        denominations = [500, 50, 20, 10, 5, 2, 1]
        result = {}
        remaining = int(amount)

        for denom in denominations:
            count = remaining // denom
            remaining = remaining % denom
            result[denom] = count

        return result
