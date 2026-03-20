# Getting Started

## Quick Setup

1. **Clone/Setup Project**
   ```bash
   cd /Users/sebblaestad/Documents/vscode/tripletex_accountning_task
   ```

2. **Create Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   cp config/.env.example .env
   # Edit .env with your Tripletex credentials
   ```

5. **Get Sandbox Account**
   - Visit https://app.ainm.no/submit/tripletex
   - Request a free sandbox account
   - You'll receive API credentials

6. **Start Server**
   ```bash
   python src/main.py
   # OR
   uvicorn src.server:app --reload
   ```

7. **Submit Endpoint**
   - Go to https://app.ainm.no/submit/tripletex
   - Enter your endpoint: `http://your-server:8000/solve`
   - Click Submit
   - Watch the leaderboard update as tasks are solved

## Development Workflow

### Understanding a Task

1. Read the task prompt carefully
2. Identify:
   - What entity to create/update (employee, invoice, etc.)
   - Required fields vs optional fields
   - Dependencies between objects
   - Multi-step workflows

### Implementing a Solver

1. Create function in appropriate task-solver file
2. Write async function that:
   - Accepts parsed parameters
   - Builds API payload
   - Makes API calls in correct order
   - Returns created object IDs
3. Add error handling
4. Add logging
5. Test with various inputs

### Testing Your Implementation

```python
# Test locally
import asyncio
from src.agents.solver import TaskSolver
from src.types.schemas import TaskRequest, TripletexCredentials

async def test():
    request = TaskRequest(
        task_prompt="Create an employee named John Doe",
        language="en",
        tripletex=TripletexCredentials(
            api_url="https://kkpqfuj-amager.tripletex.dev/v2",
            session_token="your_token",
            company_id="0",
        ),
    )
    
    solver = TaskSolver()
    response = await solver.solve(request)
    print(response)

asyncio.run(test())
```

### Debugging Tips

1. **Enable Debug Logging**
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check API Requests**
   - Print request/response in client.py
   - Use tools like Postman for manual testing

3. **Inspect Parsed Data**
   - Add prints in parser.py
   - Check extracted entities

4. **Rate Limit Issues**
   - Check X-Rate-Limit-* headers
   - Implement backoff logic

## Project Metrics

Track these as you develop:

- **Completion Rate** - % of tasks solved
- **Accuracy** - Field-by-field correctness
- **Efficiency** - API calls per task
- **Speed** - Execution time in ms

## Deployment

For production:

1. Use production Tripletex account
2. Deploy to cloud (AWS, Azure, GCP)
3. Use environment variables for secrets
4. Add logging to persistent storage
5. Set up monitoring & alerts
6. Implement rate limit handling

## Resources

- [Full Documentation](docs/ARCHITECTURE.md)
- [API Guide](docs/API_GUIDE.md)
- [Task Examples](docs/TASK_EXAMPLES.md)
- [Tripletex API](https://kkpqfuj-amager.tripletex.dev/v2-docs/)
