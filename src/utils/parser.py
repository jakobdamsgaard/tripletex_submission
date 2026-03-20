"""Utility functions for parsing and processing tasks."""

import logging
import re
from typing import Dict, Any, Optional, List

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

    detected_intents = []

    entity_patterns = {
        "employee": r"\b(ansatt|employee|worker|staff)\b",
        "customer": r"\b(kunde|customer)\b",
        "product": r"\b(produkt|product|vare|item)\b",
        "invoice": r"\b(faktura|invoice|billing)\b",
        "project": r"\b(prosjekt|project)\b",
        "travel": r"\b(reise|travel expense|travel|expense|reiseregning)\b",
        "department": r"\b(avdeling|department)\b",
    }

    action_patterns = {
        "delete": r"\b(slett|delete|remove)\b",
        "update": r"\b(oppdater|update|modify)\b",
        "create": r"\b(opprett|create|register|registrer|new)\b",
        "payment": r"\b(payment|betaling|pay)\b",
        "post": r"\b(post invoice|bokf.r|bokfør|publish invoice)\b",
    }

    for intent, pattern in entity_patterns.items():
        if re.search(pattern, prompt_lower):
            detected_intents.append(intent)

    for intent, pattern in action_patterns.items():
        if re.search(pattern, prompt_lower):
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
        "email": extract_email(prompt),
        "phone": extract_phone(prompt),
        "organization_number": extract_organization_number(prompt),
        "customer_name": extract_customer_name(prompt),
        "product_name": extract_product_name(prompt),
        "department_name": extract_department_name(prompt),
        "department_number": extract_department_number(prompt),
        "employee_name": extract_employee_name(prompt),
        "project_name": extract_project_name(prompt),
        "customer_id": extract_entity_id(prompt, "customer"),
        "employee_id": extract_entity_id(prompt, "employee"),
        "invoice_id": extract_entity_id(prompt, "invoice"),
        "project_id": extract_entity_id(prompt, "project"),
        "department_id": extract_entity_id(prompt, "department"),
        "travel_expense_id": extract_entity_id(prompt, "travel_expense"),
        "invoice_date": extract_invoice_date(prompt),
        "due_date": extract_due_date(prompt),
        "payment_date": extract_payment_date(prompt),
        "amount": extract_amount(prompt),
        "invoice_lines": extract_invoice_lines(prompt),
        "start_date": extract_start_date(prompt),
        "end_date": extract_end_date(prompt),
        "purpose": extract_purpose(prompt),
        "should_post_invoice": should_post_invoice(prompt),
        "is_project_participant_task": is_project_participant_task(prompt),
    }


def extract_customer_name(prompt: str) -> Optional[str]:
    """Extract customer name from common create-customer prompts."""
    patterns = [
        r"kunde som heter\s+(.+?)(?:\s+med|\s+with|\s*$)",
        r"kunde kalt\s+(.+?)(?:\s+med|\s+with|\s*$)",
        r"registrer en kunde som heter\s+(.+?)(?:\s+med|\s+with|\s*$)",
        r"register a customer named\s+(.+?)(?:\s+with|\s*$)",
        r"customer named\s+(.+?)(?:\s+with|\s*$)",
        r"create a customer named\s+(.+?)(?:\s+with|\s*$)",
        r"opprett kunde\s+(.+?)(?:\s+med|\s*$)",
        r"ny kunde\s+(.+?)(?:\s+med|\s*$)",
    ]

    prompt_clean = " ".join(prompt.strip().split())
    for pattern in patterns:
        match = re.search(pattern, prompt_clean, flags=re.IGNORECASE)
        if match:
            return clean_extracted_text(match.group(1))

    quoted_name = extract_quoted_value(prompt_clean)
    if quoted_name and any(keyword in prompt_clean.lower() for keyword in ["kunde", "customer"]):
        return quoted_name

    return None


def extract_department_name(prompt: str) -> Optional[str]:
    """Extract department name from create-department prompts."""
    patterns = [
        r"department called\s+(.+?)(?:\s+with|\s*$)",
        r"department named\s+(.+?)(?:\s+with|\s*$)",
        r"avdeling som heter\s+(.+?)(?:\s+med|\s*$)",
        r"avdeling kalt\s+(.+?)(?:\s+med|\s*$)",
    ]

    prompt_clean = " ".join(prompt.strip().split())
    for pattern in patterns:
        match = re.search(pattern, prompt_clean, flags=re.IGNORECASE)
        if match:
            return clean_extracted_text(match.group(1))

    quoted_name = extract_quoted_value(prompt_clean)
    if quoted_name and any(keyword in prompt_clean.lower() for keyword in ["avdeling", "department"]):
        return quoted_name

    return None


def extract_product_name(prompt: str) -> Optional[str]:
    """Extract product name from simple prompts."""
    patterns = [
        r"product named\s+(.+?)(?:\s+with|\s*$)",
        r"create a product named\s+(.+?)(?:\s+with|\s*$)",
        r"produkt som heter\s+(.+?)(?:\s+med|\s*$)",
        r"opprett et produkt som heter\s+(.+?)(?:\s+med|\s*$)",
    ]

    prompt_clean = " ".join(prompt.strip().split())
    for pattern in patterns:
        match = re.search(pattern, prompt_clean, flags=re.IGNORECASE)
        if match:
            return clean_extracted_text(match.group(1))

    quoted_name = extract_quoted_value(prompt_clean)
    if quoted_name and any(keyword in prompt_clean.lower() for keyword in ["product", "produkt"]):
        return quoted_name

    return None


def extract_employee_name(prompt: str) -> Optional[Dict[str, str]]:
    """Extract employee first and last name from simple create prompts."""
    patterns = [
        r"employee named\s+([A-ZÆØÅ][^\d,]+?)(?:\s+with|\s*$)",
        r"ansatt som heter\s+([A-ZÆØÅ][^\d,]+?)(?:\s+med|\s*$)",
        r"opprett en ansatt som heter\s+([A-ZÆØÅ][^\d,]+?)(?:\s+med|\s*$)",
        r"create an employee named\s+([A-ZÆØÅ][^\d,]+?)(?:\s+with|\s*$)",
    ]

    prompt_clean = " ".join(prompt.strip().split())
    full_name: Optional[str] = None

    for pattern in patterns:
        match = re.search(pattern, prompt_clean, flags=re.IGNORECASE)
        if match:
            full_name = clean_extracted_text(match.group(1))
            break

    if not full_name:
        quoted_name = extract_quoted_value(prompt_clean)
        if quoted_name and any(keyword in prompt_clean.lower() for keyword in ["ansatt", "employee"]):
            full_name = quoted_name

    if not full_name:
        return None

    parts = full_name.split()
    if len(parts) < 2:
        return None

    return {
        "first_name": parts[0],
        "last_name": " ".join(parts[1:]),
    }


def extract_project_name(prompt: str) -> Optional[str]:
    """Extract project name from create-project prompts."""
    patterns = [
        r"project\s+['\"]([^'\"]+)['\"]",
        r"prosjekt\s+['\"]([^'\"]+)['\"]",
        r"project called\s+(.+?)(?:\s+for customer|\s+starting|\s*$)",
        r"prosjekt som heter\s+(.+?)(?:\s+for kunde|\s+fra|\s*$)",
    ]

    prompt_clean = " ".join(prompt.strip().split())
    for pattern in patterns:
        match = re.search(pattern, prompt_clean, flags=re.IGNORECASE)
        if match:
            return clean_extracted_text(match.group(1))

    quoted_name = extract_quoted_value(prompt_clean)
    if quoted_name and any(keyword in prompt_clean.lower() for keyword in ["project", "prosjekt"]):
        return quoted_name

    return None


def extract_department_number(prompt: str) -> Optional[str]:
    """Extract department number from prompt."""
    match = re.search(
        r"(?:department number|avdelingsnummer|department no\.?|nummer)\s+(\d+)",
        prompt,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def extract_organization_number(prompt: str) -> Optional[str]:
    """Extract organization number from prompt."""
    match = re.search(
        r"(?:organization number|organisasjonsnummer)\s+(\d{9})",
        prompt,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else None


def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    match = re.search(r"[\w.+-]+@[\w.-]+\.\w+", text)
    return match.group(0) if match else None


def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    match = re.search(
        r"(?:phone|telefon|mobile|mobil)\s*(?:number|nr\.?)?\s*(?:is\s+)?[:=]?\s*(\+?\d[\d\s-]{6,}\d)",
        text,
        flags=re.IGNORECASE,
    )
    return clean_extracted_text(match.group(1)) if match else None


def extract_entity_id(prompt: str, entity: str) -> Optional[int]:
    """Extract entity ID from prompt based on entity label."""
    entity_patterns = {
        "customer": r"(?:customer|kunde)\s+(\d+)",
        "employee": r"(?:employee|ansatt)\s+(\d+)",
        "invoice": r"(?:invoice|faktura)\s+(\d+)",
        "project": r"(?:project|prosjekt)\s+(\d+)",
        "department": r"(?:department|avdeling)\s+(\d+)",
        "travel_expense": r"(?:travel expense|reiseregning|travelExpense)\s+(\d+)",
    }

    pattern = entity_patterns.get(entity)
    if not pattern:
        return None

    match = re.search(pattern, prompt, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def extract_invoice_date(text: str) -> Optional[str]:
    """Extract invoice date from prompt."""
    match = re.search(r"(?:dated|invoice date|fakturadato)\s+(\d{4}-\d{2}-\d{2})", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)

    if re.search(r"\b(invoice|faktura)\b", text, flags=re.IGNORECASE):
        dates = extract_dates(text)
        return dates[0] if dates else None

    return None


def extract_due_date(text: str) -> Optional[str]:
    """Extract due date from prompt."""
    match = re.search(r"(?:due date|forfaller|forfallsdato)\s+(\d{4}-\d{2}-\d{2})", text, flags=re.IGNORECASE)
    return match.group(1) if match else None


def extract_payment_date(text: str) -> Optional[str]:
    """Extract payment date from prompt."""
    match = re.search(r"(?:payment on|dated|betalingsdato|betalt\s+)\s+(\d{4}-\d{2}-\d{2})", text, flags=re.IGNORECASE)
    if match and re.search(r"\b(payment|betaling|pay)\b", text, flags=re.IGNORECASE):
        return match.group(1)

    dates = extract_dates(text)
    if dates and re.search(r"\b(payment|betaling|pay)\b", text, flags=re.IGNORECASE):
        return dates[0]

    return None


def extract_amount(text: str) -> Optional[float]:
    """Extract a single amount from prompt."""
    match = re.search(r"(\d+(?:[.,]\d+)?)\s*(?:NOK|kr)\b", text, flags=re.IGNORECASE)
    if not match:
        return None

    return float(match.group(1).replace(",", "."))


def extract_invoice_lines(text: str) -> List[Dict[str, Any]]:
    """Extract simple invoice lines from prompts like '10 units x 100 NOK'."""
    patterns = [
        r"(\d+(?:[.,]\d+)?)\s*(?:units?|stk|pcs?)\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*(?:NOK|kr)",
        r"(\d+(?:[.,]\d+)?)\s*[x×]\s*(\d+(?:[.,]\d+)?)\s*(?:NOK|kr)",
        r"(\d+(?:[.,]\d+)?)\s*(?:units?|stk|pcs?).{0,20}?(\d+(?:[.,]\d+)?)\s*(?:NOK|kr)",
    ]

    normalized_text = " ".join(text.strip().split())
    for pattern in patterns:
        matches = re.findall(pattern, normalized_text, flags=re.IGNORECASE)
        if matches:
            lines = []
            for index, (quantity, unit_price) in enumerate(matches, start=1):
                lines.append(
                    {
                        "description": f"Line {index}",
                        "quantity": float(quantity.replace(",", ".")),
                        "unitPrice": float(unit_price.replace(",", ".")),
                    }
                )
            return lines

    return []


def extract_start_date(text: str) -> Optional[str]:
    """Extract start date from prompts with explicit labels."""
    patterns = [
        r"(?:starting|start date|from|fra)\s+(\d{4}-\d{2}-\d{2})",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return match.group(1)

    dates = extract_dates(text)
    return dates[0] if dates else None


def extract_end_date(text: str) -> Optional[str]:
    """Extract end date from prompts with explicit labels."""
    match = re.search(r"(?:to|til|end date)\s+(\d{4}-\d{2}-\d{2})", text, flags=re.IGNORECASE)
    if match:
        return match.group(1)

    dates = extract_dates(text)
    return dates[1] if len(dates) > 1 else None


def extract_purpose(text: str) -> Optional[str]:
    """Extract a simple purpose field from travel prompts."""
    normalized_text = " ".join(text.strip().split())
    match = re.search(
        r"(?:to|til)\s+\d{4}-\d{2}-\d{2}\s+for\s+(.+)$",
        normalized_text,
        flags=re.IGNORECASE,
    )
    if match:
        return clean_extracted_text(match.group(1))

    match = re.search(r"purpose[: ]+(.+)$", normalized_text, flags=re.IGNORECASE)
    if match:
        return clean_extracted_text(match.group(1))

    return None


def should_post_invoice(text: str) -> bool:
    """Detect whether the prompt asks to post the invoice."""
    return bool(
        re.search(
            r"\b(post invoice|post the invoice|publish invoice|bokf.r|bokfør|bokfoer)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def is_project_participant_task(text: str) -> bool:
    """Detect whether the prompt adds a participant to an existing project."""
    return bool(
        re.search(
            r"\b(participant|deltaker|team member|project member)\b",
            text,
            flags=re.IGNORECASE,
        )
    )


def extract_quoted_value(text: str) -> Optional[str]:
    """Extract the first quoted value in text."""
    match = re.search(r"['\"]([^'\"]+)['\"]", text)
    return clean_extracted_text(match.group(1)) if match else None


def clean_extracted_text(value: str) -> str:
    """Normalize extracted free-form text."""
    return value.strip(" .,!?:;\"'")


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
    numbers = re.findall(r"\d+", text)
    return numbers[:5]


def extract_dates(text: str) -> List[str]:
    """Extract dates from text."""
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
