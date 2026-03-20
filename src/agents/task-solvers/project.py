"""Task solver for project-related operations."""

import logging
from typing import Dict, Any, Optional
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_project(
    client: TripletexClient,
    name: str,
    customer_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
) -> Dict[str, Any]:
    """Create project in Tripletex."""
    payload = {"name": name}

    if customer_id:
        payload["customer"] = {"id": customer_id}
    if start_date:
        payload["startDate"] = start_date
    if end_date:
        payload["endDate"] = end_date

    try:
        response = await client.post("/project", payload)
        logger.info(f"Created project: {name}")
        return response
    except Exception as e:
        logger.error(f"Error creating project: {e}")
        raise


async def add_project_participant(
    client: TripletexClient,
    project_id: int,
    employee_id: int,
) -> Dict[str, Any]:
    """Add participant to project."""
    payload = {"employee": {"id": employee_id}}

    try:
        response = await client.post(f"/project/{project_id}/participant", payload)
        logger.info(f"Added participant to project {project_id}")
        return response
    except Exception as e:
        logger.error(f"Error adding participant: {e}")
        raise
