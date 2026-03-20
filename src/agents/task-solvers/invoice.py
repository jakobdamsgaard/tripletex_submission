"""Task solver for invoice-related operations."""

import logging
from typing import Dict, Any, Optional, List
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_invoice(
    client: TripletexClient,
    customer_id: int,
    invoice_date: str,
    lines: List[Dict[str, Any]],
    due_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Create invoice in Tripletex.

    Args:
        client: Tripletex API client
        customer_id: Customer ID
        invoice_date: Invoice date (YYYY-MM-DD)
        lines: Invoice line items
        due_date: Due date (YYYY-MM-DD)

    Returns:
        Created invoice data
    """
    payload = {
        "customer": {"id": customer_id},
        "invoiceDate": invoice_date,
        "lines": lines,
    }

    if due_date:
        payload["dueDate"] = due_date

    try:
        response = await client.post("/invoice", payload)
        logger.info(f"Created invoice for customer {customer_id}")
        return response
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        raise


async def post_invoice(client: TripletexClient, invoice_id: int) -> Dict[str, Any]:
    """Post invoice to make it official."""
    try:
        response = await client.post(f"/invoice/{invoice_id}/:post", {})
        logger.info(f"Posted invoice {invoice_id}")
        return response
    except Exception as e:
        logger.error(f"Error posting invoice: {e}")
        raise


async def register_payment(
    client: TripletexClient,
    invoice_id: int,
    amount: float,
    payment_date: str,
) -> Dict[str, Any]:
    """Register payment on invoice."""
    payload = {
        "invoiceId": invoice_id,
        "amount": amount,
        "paymentDate": payment_date,
    }

    try:
        response = await client.post(f"/invoice/{invoice_id}/payment", payload)
        logger.info(f"Registered payment on invoice {invoice_id}")
        return response
    except Exception as e:
        logger.error(f"Error registering payment: {e}")
        raise
