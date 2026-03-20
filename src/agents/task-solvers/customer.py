"""Task solver for customer-related operations."""

import logging
from typing import Dict, Any, Optional
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_customer(
    client: TripletexClient,
    name: str,
    organization_number: Optional[str] = None,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> Dict[str, Any]:
    """Create customer in Tripletex.

    Args:
        client: Tripletex API client
        name: Customer name
        organization_number: Organization number
        email: Customer email
        phone: Customer phone

    Returns:
        Created customer data
    """
    payload = {"name": name}

    if organization_number:
        payload["organizationNumber"] = organization_number
    if email:
        payload["email"] = email
    if phone:
        payload["phone"] = phone

    try:
        response = await client.post("/customer", payload)
        logger.info(f"Created customer: {name}")
        return response
    except Exception as e:
        logger.error(f"Error creating customer: {e}")
        raise


async def get_customer(client: TripletexClient, customer_id: int) -> Dict[str, Any]:
    """Get customer details."""
    try:
        response = await client.get(f"/customer/{customer_id}")
        return response
    except Exception as e:
        logger.error(f"Error getting customer: {e}")
        raise


async def update_customer(
    client: TripletexClient,
    customer_id: int,
    **fields,
) -> Dict[str, Any]:
    """Update customer fields."""
    try:
        response = await client.put(f"/customer/{customer_id}", fields)
        logger.info(f"Updated customer {customer_id}")
        return response
    except Exception as e:
        logger.error(f"Error updating customer: {e}")
        raise
