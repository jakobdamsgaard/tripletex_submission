"""Global constants for Tripletex agent."""

# API Endpoints
TRIPLETEX_API_V2_URL = "https://kkpqfuj-amager.tripletex.dev/v2"

# Task Categories
TASK_CATEGORIES = {
    "employee": ["create", "update", "set_role", "contact_info"],
    "customer": ["create", "update", "delete"],
    "product": ["create", "update", "price"],
    "invoice": ["create", "post", "payment", "credit_note"],
    "travel_expense": ["register", "delete", "approve"],
    "project": ["create", "link_customer", "add_participant"],
    "department": ["create", "enable_module"],
    "corrections": ["delete", "reverse", "undo"],
}

# Supported Languages
SUPPORTED_LANGUAGES = [
    "no",  # Norwegian
    "en",  # English
    "es",  # Spanish
    "pt",  # Portuguese
    "nn",  # Nynorsk
    "de",  # German
    "fr",  # French
]

# API Limits
DEFAULT_TIMEOUT_SECONDS = 300  # 5 minutes
RATE_LIMIT_BUFFER = 10
MAX_RETRIES = 3
RETRY_BACKOFF_FACTOR = 2

# Common HTTP Status Codes
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_NO_CONTENT = 204
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_FORBIDDEN = 403
STATUS_NOT_FOUND = 404
STATUS_CONFLICT = 409
STATUS_UNPROCESSABLE = 422
STATUS_RATE_LIMIT = 429
STATUS_SERVER_ERROR = 500

# Error Codes
ERROR_CODES = {
    4000: "Bad Request Exception",
    3000: "Authentication Exception",
    9000: "Security Exception",
    6000: "Not Found Exception",
    7000: "Object Exists Exception",
    8000: "Revision Exception",
    10000: "Locked Exception",
    11000: "Illegal Filter Exception",
    14000: "Duplicate Entry",
    15000: "Value Validation Exception",
    16000: "Mapping Exception",
    17000: "Sorting Exception",
    18000: "Validation Exception",
    21000: "Param Exception",
    22000: "Invalid JSON Exception",
    23000: "Result Set Too Large Exception",
    24000: "Cryptography Exception",
    1000: "Exception",
}

# Field Specifiers
COMMON_FIELDS = {
    "employee": "id,firstName,lastName,email,phone,department,roles",
    "customer": "id,name,organizationNumber,email,phone",
    "product": "id,number,name,unit,salesUnit,costPrice,sellingPrice",
    "invoice": "id,invoiceNumber,customer,invoiceDate,dueDate,amount,status",
    "project": "id,name,customer,startDate,endDate,budget,status",
}

# Action Prefixes
ACTION_PREFIX = ":"
SUMMARY_PREFIX = ">"
