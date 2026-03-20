"""Entry point for the application."""

import asyncio
import logging
from src.agents.solver import TaskSolver
from src.types.schemas import TaskRequest, TripletexCredentials

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    """Main entry point for testing."""
    logger.info("Starting Tripletex AI Accounting Agent")

    # Example task request
    task_request = TaskRequest(
        task_prompt="Create an employee named John Doe with email john@example.com",
        language="en",
        tripletex=TripletexCredentials(
            api_url="https://kkpqfuj-amager.tripletex.dev/v2",
            session_token="test_token",
            company_id="0",
        ),
    )

    # Solve task
    solver = TaskSolver()
    response = await solver.solve(task_request)

    logger.info(f"Response: {response}")
    return response


if __name__ == "__main__":
    asyncio.run(main())
