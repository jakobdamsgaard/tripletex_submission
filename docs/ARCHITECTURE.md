# System Architecture

## Overview

The Tripletex Accounting Agent is designed to solve accounting tasks by:

1. **Receiving** a task prompt in one of 7 languages
2. **Parsing** the prompt to understand intent and extract parameters
3. **Executing** API calls to complete the task
4. **Validating** results against expected outcomes
5. **Returning** scored completion status

## Component Structure

```
┌─────────────────────────────────────────┐
│         FastAPI Server                   │
│         POST /solve endpoint             │
└────────────┬────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────┐
│    TaskSolver (Orchestrator)            │
│  - Route to appropriate solver           │
│  - Track API calls & timing              │
│  - Aggregate results                     │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┬──────────┬────────────┬─────────┐
    ▼                 ▼          ▼            ▼         ▼
┌────────┐     ┌──────────┐  ┌────────┐  ┌────────┐ ┌──────────┐
│Employee│     │Customer  │  │Invoice │  │Project │ │Travel    │
│Solver  │     │Solver    │  │Solver  │  │Solver  │ │Expense   │
└────────┘     └──────────┘  └────────┘  └────────┘ │Solver    │
    │              │            │            │      └──────────┘
    └──────────────┼────────────┼────────────┘
                   ▼
    ┌──────────────────────────────────┐
    │  Tripletex API Client            │
    │  - HTTP requests                 │
    │  - Authentication                │
    │  - Error handling                │
    │  - Rate limiting                 │
    └────────────┬─────────────────────┘
                 │
                 ▼
    ┌──────────────────────────────────┐
    │  Tripletex API v2                │
    │  https://tripletex.dev/v2        │
    └──────────────────────────────────┘
```

## Data Flow

### Task Execution

1. **Request Reception**
   ```json
   {
     "task_prompt": "Create an employee named...",
     "language": "en",
     "attachments": ["file.pdf"],
     "tripletex": {
       "api_url": "...",
       "session_token": "...",
       "company_id": "0"
     }
   }
   ```

2. **Task Parsing**
   - Extract intent (create, update, delete, etc.)
   - Extract entities (names, dates, amounts)
   - Process any attachments (PDFs/images)

3. **API Execution**
   - Initialize Tripletex client
   - Execute task-specific solver
   - Make sequential API calls
   - Collect results

4. **Response Compilation**
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

## Module Responsibilities

### Server (`src/server.py`)
- FastAPI application
- `/solve` endpoint implementation
- Request/response handling
- Error handling & logging

### TaskSolver (`src/agents/solver.py`)
- Task routing orchestration
- Calls appropriate task-specific solver
- Tracks metrics (API calls, timing)
- Aggregates results

### Task Solvers (`src/agents/task-solvers/`)
Each solver handles a specific domain:
- `employee.py` - Employee management
- `customer.py` - Customer management
- `invoice.py` - Invoice & billing
- `project.py` - Project management
- `travel.py` - Travel expenses
- `corrections.py` - Deletions & reversals
- `department.py` - Department setup

### API Client (`src/api/client.py`)
- HTTP request execution
- Authentication header management
- Error response handling
- Rate limit respect
- Async request handling

### Utilities
- `parser.py` - Intent & entity extraction
- `file_handler.py` - PDF/image processing
- `validators.py` - Response validation
- `schemas.py` - Pydantic models

## Key Design Decisions

### Async/Await
- All I/O operations are async
- Allows concurrent request handling
- Efficient resource usage

### Type Safety
- Pydantic models for all requests/responses
- Type hints throughout
- Validation at API boundaries

### Error Handling
- Custom exception classes
- Detailed error logging
- Graceful failure with informative messages

### Extensibility
- Task solvers are isolated modules
- Easy to add new task types
- Plugin-like architecture

## Sequence Diagram: Employee Creation

```
Client          Server          Solver          API Client      Tripletex
  │                │                │                │              │
  ├─ POST /solve ─>│                │                │              │
  │                │─ parse task ─>│                │              │
  │                │<─return parsed                 │              │
  │                │                │                │              │
  │                │─ solve task ───>                │              │
  │                │                │─ create auth ─>               │
  │                │                │                │              │
  │                │                │─ POST /employee ->           │
  │                │                │                │─ /employee─>
  │                │                │                │<─ 201 OK ──
  │                │                │<─ response ────│              │
  │                │<─ results ─────│                │              │
  │<─ response ────│                │                │              │
  │                │                │                │              │
```

## Performance Considerations

1. **API Rate Limiting**
   - Respect X-Rate-Limit-* headers
   - Implement backoff for rate limit errors
   - Batch requests when possible

2. **Timeout Management**
   - 5-minute absolute timeout per task
   - Short individual request timeouts
   - Early detection of slow operations

3. **Resource Cleanup**
   - Close HTTP clients gracefully
   - Free file resources after processing
   - Clear caches periodically

## Testing Strategy

1. **Unit Tests**
   - Test parsers with various inputs
   - Test validators with edge cases
   - Test error handling

2. **Integration Tests**
   - Test with Tripletex sandbox
   - Test complete task workflows
   - Test error recovery

3. **Performance Tests**
   - Measure execution time
   - Track API call count
   - Monitor resource usage

## Future Enhancements

- [ ] LLM-based intent classification
- [ ] Multi-language prompt understanding
- [ ] Vision API for document analysis
- [ ] Caching of repeated queries
- [ ] Task templating system
- [ ] Audit logging to database
