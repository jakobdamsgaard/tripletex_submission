"""FastAPI server with /solve endpoint."""

import logging
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from src.types.schemas import TaskRequest, TaskResponse, TripletexCredentials
from src.agents.solver import TaskSolver
from config.settings import get_settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def _mask_secret(value: str | None) -> str:
    """Mask sensitive values in logs."""
    if not value:
        return "[missing]"
    if len(value) <= 8:
        return "[redacted]"
    return f"{value[:4]}...{value[-4:]}"

# Initialize FastAPI app
app = FastAPI(
    title="Tripletex AI Agent",
    description="AI agent for solving accounting tasks in Tripletex",
    version="1.0.0",
)

# Initialize task solver
solver = TaskSolver()


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "tripletex-agent"}


@app.get("/")
async def root():
    """Root endpoint for basic uptime checks."""
    return {
        "status": "ok",
        "service": "tripletex-agent",
        "endpoints": ["/health", "/solve"],
    }


@app.post("/solve", response_model=TaskResponse)
async def solve_task(request: TaskRequest) -> TaskResponse:
    """Solve an accounting task.

    Args:
        request: Task request with prompt and Tripletex credentials

    Returns:
        Task response with results
    """
    try:
        settings = get_settings()
        api_url = request.tripletex.api_url if request.tripletex and request.tripletex.api_url else settings.tripletex_api_url
        session_token = (
            request.tripletex.session_token
            if request.tripletex and request.tripletex.session_token
            else settings.tripletex_session_token
        )
        company_id = (
            request.tripletex.company_id
            if request.tripletex and request.tripletex.company_id
            else settings.tripletex_company_id
        )

        if not api_url or not session_token:
            raise HTTPException(
                status_code=400,
                detail="Missing Tripletex credentials. Provide them in the request or configure .env.",
            )

        request = request.model_copy(
            update={
                "tripletex": TripletexCredentials(
                    api_url=api_url,
                    session_token=session_token,
                    company_id=company_id,
                )
            }
        )

        logger.info("Received task in language: %s", request.language)
        logger.info("Task prompt: %s", request.task_prompt)
        logger.info(
            "Tripletex credentials api_url=%r company_id=%r session_token=%s",
            request.tripletex.api_url,
            request.tripletex.company_id,
            _mask_secret(request.tripletex.session_token),
        )

        # Solve the task
        response = await solver.solve(request)

        logger.info("Task completed with status: %s", response.status)
        return response

    except Exception as e:
        logger.exception(f"Error processing task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler."""
    logger.exception(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "status": "failed",
            "error": "Internal server error",
        },
    )


if __name__ == "__main__":
    import uvicorn

    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.server_host,
        port=settings.server_port,
        log_level=settings.log_level.lower(),
    )
