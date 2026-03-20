"""Utility functions for parsing and processing tasks."""

import logging
import json
from typing import Dict, Any, Optional, List
from pathlib import Path

logger = logging.getLogger(__name__)


def parse_task_prompt(prompt: str, language: str = "en") -> Dict[str, Any]:
    """Parse task prompt to extract intent and parameters.

    Args:
        prompt: Task prompt text
        language: Language of the prompt

    Returns:
        Parsed task information
    """
    return {
        "raw_prompt": prompt,
        "language": language,
        "intent": extract_intent(prompt),
        "entities": extract_entities(prompt),
    }


def extract_intent(prompt: str) -> str:
    """Extract task intent from prompt.

    Args:
        prompt: Task prompt text

    Returns:
        Task intent (e.g., "create_employee", "register_invoice")
    """
    # Simple keyword-based intent extraction
    # In production, use NLP models
    prompt_lower = prompt.lower()

    intent_keywords = {
        "employee": ["ansatt", "employee", "worker", "staff"],
        "customer": ["kunde", "customer", "client"],
        "product": ["produkt", "product", "vare", "item"],
        "invoice": ["faktura", "invoice", "billing"],
        "project": ["prosjekt", "project"],
        "travel": ["reise", "travel", "expense"],
        "department": ["avdeling", "department"],
        "delete": ["slett", "delete", "remove"],
        "update": ["oppdater", "update", "modify"],
        "create": ["opprett", "create", "new"],
    }

    detected_intents = []
    for intent, keywords in intent_keywords.items():
        if any(kw in prompt_lower for kw in keywords):
            detected_intents.append(intent)

    return ",".join(detected_intents) if detected_intents else "unknown"


def extract_entities(prompt: str) -> Dict[str, Any]:
    """Extract named entities from prompt.

    Args:
        prompt: Task prompt text

    Returns:
        Extracted entities
    """
    # Placeholder for more sophisticated entity extraction
    return {
        "names": extract_names(prompt),
        "numbers": extract_numbers(prompt),
        "dates": extract_dates(prompt),
    }


def extract_names(text: str) -> List[str]:
    """Extract potential names from text."""
    # Simple pattern matching - in production use NER
    names = []
    words = text.split()
    for i, word in enumerate(words):
        if word[0].isupper() and len(word) > 2:
            names.append(word)
    return names[:5]  # Limit to first 5


def extract_numbers(text: str) -> List[str]:
    """Extract potential numbers/IDs from text."""
    import re

    numbers = re.findall(r"\d+", text)
    return numbers[:5]


def extract_dates(text: str) -> List[str]:
    """Extract dates from text."""
    import re

    # ISO 8601 pattern
    dates = re.findall(r"\d{4}-\d{2}-\d{2}", text)
    return dates


def validate_api_response(response: Dict[str, Any], expected_fields: List[str]) -> bool:
    """Validate API response contains expected fields.

    Args:
        response: API response data
        expected_fields: List of field names to check

    Returns:
        True if all expected fields present
    """
    if "value" in response:
        response = response["value"]

    for field in expected_fields:
        if field not in response:
            logger.warning(f"Missing expected field in response: {field}")
            return False

    return True


def build_query_string(
    from_: int = 0,
    count: int = 100,
    sorting: Optional[str] = None,
    fields: Optional[str] = None,
) -> Dict[str, Any]:
    """Build query parameters for API calls.

    Args:
        from_: Starting index for pagination
        count: Number of results to return
        sorting: Sort order (e.g., "-date")
        fields: Fields to return

    Returns:
        Query parameters dict
    """
    params = {"from": from_, "count": count}

    if sorting:
        params["sorting"] = sorting

    if fields:
        params["fields"] = fields

    return params
