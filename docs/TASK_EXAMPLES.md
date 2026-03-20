# Test Examples & Task Solutions

## Employee Tasks

### Example 1: Create Simple Employee

**Prompt:**  
"Create an employee named John Smith with email john.smith@company.com"

**Solution:**
```python
# 1. Parse prompt
{
    "intent": "create_employee",
    "firstName": "John",
    "lastName": "Smith",
    "email": "john.smith@company.com"
}

# 2. API call
POST /employee HTTP/1.1
{
    "firstName": "John",
    "lastName": "Smith",
    "email": "john.smith@company.com"
}

# 3. Expected response
{
    "value": {
        "id": 123,
        "firstName": "John",
        "lastName": "Smith",
        "email": "john.smith@company.com"
    }
}
```

### Example 2: Update Employee Department

**Prompt:**  
"Update employee 456 to work in department 789"

**Solution:**
```python
PUT /employee/456 HTTP/1.1
{
    "department": {
        "id": 789
    }
}
```

## Customer Tasks

### Example 1: Register Customer

**Prompt:**  
"Register a customer named Beta AS with organization number 987654321"

**Solution:**
```python
POST /customer HTTP/1.1
{
    "name": "Beta AS",
    "organizationNumber": "987654321"
}
```

### Example 2: Add Contact Info

**Prompt:**  
"Update customer 100 with email contact@betaas.no and phone +47 123 45 678"

**Solution:**
```python
PUT /customer/100 HTTP/1.1
{
    "email": "contact@betaas.no",
    "phone": "+47 123 45 678"
}
```

## Invoice Tasks

### Example 1: Create and Post Invoice

**Prompt:**  
"Create invoice for customer 50 dated 2026-03-15 with two lines: 10 units × 100 NOK and 5 units × 200 NOK"

**Solution:**
```python
# Step 1: Create invoice
POST /invoice HTTP/1.1
{
    "customer": {"id": 50},
    "invoiceDate": "2026-03-15",
    "lines": [
        {
            "quantity": 10.0,
            "unitPrice": 100.0,
            "description": "Product A"
        },
        {
            "quantity": 5.0,
            "unitPrice": 200.0,
            "description": "Product B"
        }
    ]
}

# Step 2: Post the invoice
POST /invoice/{invoiceId}/:post HTTP/1.1

# Step 3: Expected result
{
    "id": 201,
    "invoiceNumber": 1001,
    "invoiceDate": "2026-03-15",
    "amount": 2000.0  // (10×100 + 5×200)
}
```

### Example 3: Register Payment

**Prompt:**  
"Register a 1500 NOK payment on invoice 201 dated 2026-03-20"

**Solution:**
```python
POST /invoice/201/payment HTTP/1.1
{
    "amount": 1500.0,
    "paymentDate": "2026-03-20"
}
```

## Project Tasks

### Example 1: Create Project with Customer Link

**Prompt:**  
"Create a project 'Website Redesign' for customer 50, starting 2026-04-01"

**Solution:**
```python
POST /project HTTP/1.1
{
    "name": "Website Redesign",
    "customer": {"id": 50},
    "startDate": "2026-04-01"
}
```

### Example 2: Add Team Member to Project

**Prompt:**  
"Add employee 123 as participant to project 10"

**Solution:**
```python
POST /project/10/participant HTTP/1.1
{
    "employee": {"id": 123}
}
```

## Travel Expense Tasks

### Example 1: Register Travel Expense

**Prompt:**  
"Register travel expense for employee 100 from 2026-04-10 to 2026-04-12 for client visit"

**Solution:**
```python
POST /travelExpense HTTP/1.1
{
    "employee": {"id": 100},
    "startDate": "2026-04-10",
    "endDate": "2026-04-12",
    "purpose": "Client visit"
}
```

## Correction Tasks

### Example 1: Delete Incorrect Entry

**Prompt:**  
"Delete customer 999 that was created by mistake"

**Solution:**
```python
DELETE /customer/999 HTTP/1.1
```

### Example 2: Delete Invoice

**Prompt:**  
"Remove invoice 500 that is no longer valid"

**Solution:**
```python
DELETE /invoice/500 HTTP/1.1
```

## Department Tasks

### Example 1: Create Department

**Prompt:**  
"Create a department called 'Sales' with department number 100"

**Solution:**
```python
POST /department HTTP/1.1
{
    "name": "Sales",
    "number": "100"
}
```

## Multi-step Workflows

### Example 1: Complete Order Process

**Prompt:**  
"Create a new customer 'TechCorp', then create a project for them, and add employee 5 to the project"

**Solution:**
```python
# Step 1: Create customer
POST /customer HTTP/1.1
{
    "name": "TechCorp"
}
# Response: {"id": 501}

# Step 2: Create project
POST /project HTTP/1.1
{
    "name": "TechCorp Project",
    "customer": {"id": 501}
}
# Response: {"id": 12}

# Step 3: Add participant
POST /project/12/participant HTTP/1.1
{
    "employee": {"id": 5}
}
```

## Testing Tips

1. **Language Variations**
   - Test with Norwegian prompts
   - Test with English prompts
   - Handle abbreviations and aliases

2. **Data Extraction**
   - Extract dates in ISO format (YYYY-MM-DD)
   - Parse numbers and currency amounts
   - Handle organization numbers and IDs

3. **Error Cases**
   - Invalid IDs (404 Not Found)
   - Missing required fields (422 Unprocessable)
   - Duplicate entries (409 Conflict)

4. **Edge Cases**
   - Empty responses
   - Very large datasets
   - Special characters in names
   - Multiple simultaneous requests

## Scoring Criteria

Tasks are scored on:

1. **Correctness** (0.0 - 1.0)
   - All required fields created
   - Values match expected values
   - Relationships established properly

2. **Completeness** (0.0 - 0.5)
   - All task steps executed
   - All objects created/updated

3. **Efficiency** (0.0 - 5.0)
   - Fewer unnecessary API calls
   - Faster execution time
   - Optimal use of batch operations

**Total Score Range:** 0.0 (failed) - 6.0 (perfect)
