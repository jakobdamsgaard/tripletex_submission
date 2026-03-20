"""Task solver for department operations."""

import logging
from typing import Dict, Any, Optional
from src.api.client import TripletexClient

logger = logging.getLogger(__name__)


async def create_department(
    client: TripletexClient,
    name: str,
    number: Optional[str] = None,
) -> Dict[str, Any]:
    """Create department in Tripletex."""
    payload = {"name": name}

    if number:
        payload["number"] = number

    try:
        response = await client.post("/department", payload)
        logger.info(f"Created department: {name}")
        return response
    except Exception as e:
        logger.error(f"Error creating department: {e}")
        raise


async def enable_accounting_module(
    client: TripletexClient,
    module_name: str,
) -> Dict[str, Any]:
    """Enable accounting module for company."""
    # This would typically be done via company settings
    logger.warning("Enable module functionality needs implementation")
    return {}
