"""Task solver for corrections and deletions."""

import logging
from typing import Dict, Any
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def delete_employee(client: TripletexClient, employee_id: int) -> Dict[str, Any]:
    """Delete employee from Tripletex."""
    try:
        response = await client.delete(f"/employee/{employee_id}")
        logger.info(f"Deleted employee {employee_id}")
        return response
    except Exception as e:
        logger.error(f"Error deleting employee: {e}")
        raise


async def delete_invoice(client: TripletexClient, invoice_id: int) -> Dict[str, Any]:
    """Delete invoice from Tripletex."""
    try:
        response = await client.delete(f"/invoice/{invoice_id}")
        logger.info(f"Deleted invoice {invoice_id}")
        return response
    except Exception as e:
        logger.error(f"Error deleting invoice: {e}")
        raise


async def delete_customer(client: TripletexClient, customer_id: int) -> Dict[str, Any]:
    """Delete customer from Tripletex."""
    try:
        response = await client.delete(f"/customer/{customer_id}")
        logger.info(f"Deleted customer {customer_id}")
        return response
    except Exception as e:
        logger.error(f"Error deleting customer: {e}")
        raise


async def reverse_entry(
    client: TripletexClient,
    entry_type: str,
    entry_id: int,
) -> Dict[str, Any]:
    """Reverse an accounting entry."""
    # Implementation depends on entry type
    logger.warning(f"Reverse entry not fully implemented for {entry_type}")
    return {}
