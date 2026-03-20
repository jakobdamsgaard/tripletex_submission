"""API endpoint definitions and helpers."""

# Employee endpoints
EMPLOYEE = "/employee"
EMPLOYEE_BY_ID = "/employee/{id}"
EMPLOYEE_CREATE = "/employee"

# Customer endpoints
CUSTOMER = "/customer"
CUSTOMER_BY_ID = "/customer/{id}"
CUSTOMER_CREATE = "/customer"

# Product endpoints
PRODUCT = "/product"
PRODUCT_BY_ID = "/product/{id}"
PRODUCT_CREATE = "/product"

# Invoice endpoints
INVOICE = "/invoice"
INVOICE_BY_ID = "/invoice/{id}"
INVOICE_CREATE = "/invoice"
INVOICE_POST = "/invoice/{id}/:post"
INVOICE_PAYMENT = "/invoice/{id}/payment"

# Project endpoints
PROJECT = "/project"
PROJECT_BY_ID = "/project/{id}"
PROJECT_CREATE = "/project"
PROJECT_PARTICIPANT = "/project/{id}/participant"

# Department endpoints
DEPARTMENT = "/department"
DEPARTMENT_BY_ID = "/department/{id}"
DEPARTMENT_CREATE = "/department"

# Travel expense endpoints
TRAVEL_EXPENSE = "/travelExpense"
TRAVEL_EXPENSE_BY_ID = "/travelExpense/{id}"
TRAVEL_EXPENSE_CREATE = "/travelExpense"

# General endpoints
COMPANY = "/company"
COMPANY_INFO = "/company/>withLoginAccess"

# Utility endpoints
TOKEN_SESSION_CREATE = "/token/session/:create"


def format_endpoint(template: str, **kwargs) -> str:
    """Format endpoint with parameters.

    Args:
        template: Endpoint template
        **kwargs: Parameters to substitute

    Returns:
        Formatted endpoint
    """
    return template.format(**kwargs)
