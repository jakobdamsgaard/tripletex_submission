"""Validation utilities for API responses and task completions."""

import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


def validate_employee(employee_data: Dict[str, Any]) -> bool:
    """Validate employee object has required fields.

    Args:
        employee_data: Employee object to validate

    Returns:
        True if valid
    """
    required_fields = ["firstName", "lastName"]
    return all(field in employee_data for field in required_fields)


def validate_customer(customer_data: Dict[str, Any]) -> bool:
    """Validate customer object has required fields.

    Args:
        customer_data: Customer object to validate

    Returns:
        True if valid
    """
    required_fields = ["name"]
    return all(field in customer_data for field in required_fields)


def validate_invoice(invoice_data: Dict[str, Any]) -> bool:
    """Validate invoice object has required fields.

    Args:
        invoice_data: Invoice object to validate

    Returns:
        True if valid
    """
    required_fields = ["customer", "invoiceDate"]
    return all(field in invoice_data for field in required_fields)


def validate_api_error_response(response: Dict[str, Any]) -> bool:
    """Check if response is an error.

    Args:
        response: API response

    Returns:
        True if error
    """
    return "status" in response and "code" in response and response.get("status", 0) >= 400


def validate_response_envelope(response: Dict[str, Any]) -> bool:
    """Validate response follows Tripletex envelope format.

    Args:
        response: API response

    Returns:
        True if valid envelope
    """
    if "value" in response:
        # Single value response
        return True
    elif "values" in response:
        # Multiple values response
        return True
    elif "status" in response and "code" in response:
        # Error response
        return True

    logger.warning(f"Response does not match expected envelope format: {response}")
    return False


def compare_field_values(
    actual: Any,
    expected: Any,
    field_name: str,
) -> tuple[bool, Optional[str]]:
    """Compare actual vs expected field values.

    Args:
        actual: Actual value
        expected: Expected value
        field_name: Field name for logging

    Returns:
        Tuple of (match, error_message)
    """
    if actual == expected:
        return True, None

    # Type-specific comparisons
    if isinstance(expected, (int, float)):
        try:
            actual_num = float(actual)
            expected_num = float(expected)
            if abs(actual_num - expected_num) < 0.01:  # Small tolerance
                return True, None
        except (ValueError, TypeError):
            pass

    error = f"Field {field_name}: expected {expected}, got {actual}"
    return False, error


def score_completion(
    task_results: Dict[str, Any],
    expected_results: Dict[str, Any],
) -> float:
    """Score task completion (0.0 - 1.0).

    Args:
        task_results: Actual task results
        expected_results: Expected task results

    Returns:
        Score from 0.0 to 1.0
    """
    if not expected_results:
        return 0.0 if task_results else 1.0

    matches = 0
    total = 0

    for key, expected_value in expected_results.items():
        total += 1
        actual_value = task_results.get(key)
        match, _ = compare_field_values(actual_value, expected_value, key)
        if match:
            matches += 1

    return matches / total if total > 0 else 0.0
