# Tripletex API Integration Guide

## Authentication

The Tripletex API uses **Basic Authentication** with a combination of:
- `company_id`: Target company (0 = own company)
- `session_token`: Session token from authentication

### Creating Auth Header

```python
import base64

company_id = "0"
session_token = "your_session_token"
auth_string = f"{company_id}:{session_token}"
encoded = base64.b64encode(auth_string.encode()).decode()
auth_header = f"Basic {encoded}"
```

## Common API Patterns

### GET Request with Fields Parameter

```python
# Specify which fields to return
response = await client.get(
    "/employee/123",
    fields="id,firstName,lastName,email,phone"
)
```

### Pagination

```python
response = await client.get(
    "/employee",
    params={"from": 0, "count": 100}
)
# Returns: {"fullResultSize": N, "from": 0, "count": 100, "values": [...]}
```

### Sorting

```python
response = await client.get(
    "/invoice",
    params={"sorting": "-invoiceDate"}  # Descending by date
)
```

### API Actions

Actions are prefixed with `:` in the URL:

```python
# Post an invoice
await client.post(f"/invoice/{invoice_id}/:post", {})

# Approve a voucher
await client.post(f"/ledger/voucher/{voucher_id}/:approve", {})
```

### Summaries/Aggregations

Summaries are prefixed with `>`:

```python
# Get companies with login access
response = await client.get("/company/>withLoginAccess")
```

## Error Handling

### Response Format

```json
{
  "status": 400,
  "code": 15000,
  "message": "Invalid input",
  "developerMessage": "Field validation failed",
  "validationMessages": [
    {"field": "email", "message": "Invalid email format"}
  ],
  "requestId": "abc-123"
}
```

### Rate Limiting

Check response headers:
- `X-Rate-Limit-Limit`: Total allowed requests
- `X-Rate-Limit-Remaining`: Remaining requests
- `X-Rate-Limit-Reset`: Seconds until reset

HTTP 429 means rate limit exceeded.

## Task Implementation Checklist

For each task solver:

- [ ] Parse the task prompt to extract parameters
- [ ] Validate input data
- [ ] Sequential API calls in correct order
- [ ] Handle errors gracefully
- [ ] Log all actions
- [ ] Return created/updated object IDs
- [ ] Test with different languages and datasets

## Resources

- [API Documentation](https://kkpqfuj-amager.tripletex.dev/v2-docs/)
- [GitHub Repository](https://github.com/Tripletex/tripletex-api2)
- [Developer Portal](https://developer.tripletex.no/)
