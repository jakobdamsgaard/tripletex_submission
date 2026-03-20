"""Task solver for travel expense operations."""

import logging
from typing import Dict, Any, Optional
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_travel_expense(
    client: TripletexClient,
    employee_id: int,
    start_date: str,
    end_date: Optional[str] = None,
    purpose: Optional[str] = None,
) -> Dict[str, Any]:
    """Register travel expense in Tripletex."""
    payload = {
        "employee": {"id": employee_id},
        "startDate": start_date,
    }

    if end_date:
        payload["endDate"] = end_date
    if purpose:
        payload["purpose"] = purpose

    try:
        response = await client.post("/travelExpense", payload)
        logger.info(f"Created travel expense for employee {employee_id}")
        return response
    except Exception as e:
        logger.error(f"Error creating travel expense: {e}")
        raise


async def delete_travel_expense(
    client: TripletexClient,
    expense_id: int,
) -> Dict[str, Any]:
    """Delete travel expense."""
    try:
        response = await client.delete(f"/travelExpense/{expense_id}")
        logger.info(f"Deleted travel expense {expense_id}")
        return response
    except Exception as e:
        logger.error(f"Error deleting travel expense: {e}")
        raise
