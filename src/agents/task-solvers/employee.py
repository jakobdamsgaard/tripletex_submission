"""Example task solver for employee tasks."""

import logging
from typing import Dict, Any
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_employee(
    client: TripletexClient,
    first_name: str,
    last_name: str,
    email: Optional[str] = None,
    phone: Optional[str] = None,
) -> Dict[str, Any]:
    """Create employee in Tripletex.

    Args:
        client: Tripletex API client
        first_name: Employee first name
        last_name: Employee last name
        email: Employee email
        phone: Employee phone

    Returns:
        Created employee data
    """
    payload = {
        "firstName": first_name,
        "lastName": last_name,
    }

    if email:
        payload["email"] = email

    if phone:
        payload["phone"] = phone

    try:
        response = await client.post("/employee", payload)
        logger.info(f"Created employee: {first_name} {last_name}")
        return response
    except Exception as e:
        logger.error(f"Error creating employee: {e}")
        raise


async def get_employee(client: TripletexClient, employee_id: int) -> Dict[str, Any]:
    """Get employee details.

    Args:
        client: Tripletex API client
        employee_id: Employee ID

    Returns:
        Employee data
    """
    try:
        response = await client.get(f"/employee/{employee_id}")
        return response
    except Exception as e:
        logger.error(f"Error getting employee: {e}")
        raise


async def update_employee(
    client: TripletexClient,
    employee_id: int,
    **fields,
) -> Dict[str, Any]:
    """Update employee fields.

    Args:
        client: Tripletex API client
        employee_id: Employee ID
        **fields: Fields to update

    Returns:
        Updated employee data
    """
    try:
        response = await client.put(f"/employee/{employee_id}", fields)
        logger.info(f"Updated employee {employee_id}")
        return response
    except Exception as e:
        logger.error(f"Error updating employee: {e}")
        raise
