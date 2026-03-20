# Tripletex AI Accounting Agent

An intelligent agent that solves accounting tasks in Tripletex using the REST API. The agent receives task prompts in multiple languages and uses LLM reasoning to complete complex accounting workflows.

## Overview

- **Task Types**: 30 different accounting task categories
- **Variants**: 56 per task (7 languages × 8 datasets)
- **Timeout**: 5 minutes per submission
- **Scoring**: Field-by-field verification + efficiency bonus
- **Supported Languages**: Norwegian, English, Spanish, Portuguese, Nynorsk, German, French

## Task Categories

- Employees (create, update roles, contact info)
- Customers & Products
- Invoicing & Payments
- Travel Expenses
- Projects & Departments
- Corrections & Deletions

## Project Structure

```
src/
├── api/                    # Tripletex API client
│   ├── client.py          # Main API client wrapper
│   ├── auth.py            # Authentication handling
│   └── endpoints.py       # API endpoint definitions
├── agents/                # AI agent logic
│   ├── solver.py          # Main task solver orchestrator
│   └── task-solvers/      # Task-specific handlers
│       ├── employee.py
│       ├── customer.py
│       ├── invoice.py
│       ├── travel.py
│       ├── project.py
│       └── corrections.py
├── utils/                 # Utility functions
│   ├── parser.py          # Parse task prompts
│   ├── file_handler.py    # Handle PDF/image attachments
│   └── validators.py      # Validate API responses
├── types/                 # Type definitions
│   └── schemas.py         # Pydantic models for API objects
├── server.py              # FastAPI /solve endpoint
└── main.py                # Entry point

config/
├── settings.py            # Configuration management
├── .env.example           # Environment variables template
└── constants.py           # API constants & defaults

tests/
├── test_api.py
├── test_agents.py
└── fixtures/              # Test data & mocks

docs/
├── API_GUIDE.md           # Tripletex API usage guide
├── TASK_EXAMPLES.md       # Task examples & solutions
└── ARCHITECTURE.md        # System design documentation
```

## Installation

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file based on `.env.example`:

```env
TRIPLETEX_API_URL=https://kkpqfuj-amager.tripletex.dev/v2
CONSUMER_TOKEN=your_consumer_token
EMPLOYEE_TOKEN=your_employee_token
LOG_LEVEL=INFO
```

## Running

```bash
python src/main.py
# OR
uvicorn src.server:app --reload
```

The agent will listen on `http://localhost:8000/solve` for POST requests.

## Request Format

```json
{
  "task_prompt": "Create an employee named...",
  "language": "en",
  "attachments": ["file1.pdf"],
  "tripletex": {
    "api_url": "...",
    "session_token": "...",
    "company_id": "0"
  }
}
```

## Response Format

```json
{
  "status": "completed",
  "result": {
    "created_objects": [...],
    "api_calls": 5,
    "execution_time_ms": 2340
  }
}
```

## Key Implementation Details

- **LLM Integration**: Uses Claude/GPT for task interpretation
- **API Proxy**: All Tripletex API calls go through authenticated proxy
- **Rate Limiting**: Respects X-Rate-Limit-* headers
- **Error Handling**: Graceful fallbacks and retry logic
- **Multi-language**: Task prompts in 7 languages
- **File Support**: Handles PDF/image attachments when needed

## Development

Run tests:
```bash
pytest tests/ -v
```

## Resources

- [Tripletex API Documentation](https://kkpqfuj-amager.tripletex.dev/v2-docs/)
- [Task Documentation](https://app.ainm.no/docs/tripletex/overview)
- [GitHub API Reference](https://github.com/Tripletex/tripletex-api2)
# Tripletex_accounting_task
