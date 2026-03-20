"""Main task solver orchestrator."""

import logging
import time
from typing import Dict, Any, Optional
from src.api.client import TripletexClient
from src.types.schemas import TaskRequest, TaskResponse, TaskResult
from src.utils.parser import parse_task_prompt
from src.utils.file_handler import process_attachments

logger = logging.getLogger(__name__)


class TaskSolver:
    """Main orchestrator for solving accounting tasks."""

    def __init__(self):
        """Initialize task solver."""
        self.client: Optional[TripletexClient] = None
        self.api_calls = 0
        self.start_time = 0

    async def solve(self, request: TaskRequest) -> TaskResponse:
        """Solve a task.

        Args:
            request: Task request with prompt and credentials

        Returns:
            Response with status and results
        """
        self.start_time = time.time()
        self.api_calls = 0

        try:
            # Initialize Tripletex client
            self.client = TripletexClient(
                api_url=request.tripletex.api_url,
                session_token=request.tripletex.session_token,
                company_id=request.tripletex.company_id,
            )

            # Parse task
            task_info = parse_task_prompt(request.task_prompt, request.language)
            logger.info(f"Parsed task intent: {task_info['intent']}")

            # Process attachments if any
            attachments = {}
            if request.attachments:
                attachments = await process_attachments(request.attachments)
                logger.info(f"Processed {len(attachments)} attachments")

            # Solve the task
            result = await self._solve_task(task_info, attachments)

            execution_time = int((time.time() - self.start_time) * 1000)

            return TaskResponse(
                status="completed",
                result=TaskResult(
                    created_objects=result.get("created_objects"),
                    updated_objects=result.get("updated_objects"),
                    deleted_objects=result.get("deleted_objects"),
                    api_calls=self.api_calls,
                    execution_time_ms=execution_time,
                    success=True,
                ),
            )

        except Exception as e:
            logger.exception(f"Error solving task: {e}")
            execution_time = int((time.time() - self.start_time) * 1000)

            return TaskResponse(
                status="failed",
                error=str(e),
                result=TaskResult(
                    api_calls=self.api_calls,
                    execution_time_ms=execution_time,
                    success=False,
                    message=str(e),
                ),
            )

        finally:
            if self.client:
                await self.client.close()

    async def _solve_task(self, task_info: Dict[str, Any], attachments: Dict[str, Any]) -> Dict[str, Any]:
        """Solve a specific task.

        Args:
            task_info: Parsed task information
            attachments: Processed attachments

        Returns:
            Task results with created/updated objects
        """
        intent = task_info["intent"]
        prompt = task_info["raw_prompt"]

        # Route to appropriate solver based on intent
        if "employee" in intent:
            return await self._solve_employee_task(prompt, task_info)
        elif "customer" in intent:
            return await self._solve_customer_task(prompt, task_info)
        elif "invoice" in intent:
            return await self._solve_invoice_task(prompt, task_info)
        elif "project" in intent:
            return await self._solve_project_task(prompt, task_info)
        elif "travel" in intent:
            return await self._solve_travel_task(prompt, task_info)
        elif "department" in intent:
            return await self._solve_department_task(prompt, task_info)
        else:
            logger.warning(f"Unknown task intent: {intent}")
            return {}

    async def _solve_employee_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve employee-related tasks."""
        logger.info("Solving employee task")
        # TODO: Implement employee task solving
        return {"created_objects": []}

    async def _solve_customer_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve customer-related tasks."""
        logger.info("Solving customer task")
        # TODO: Implement customer task solving
        return {"created_objects": []}

    async def _solve_invoice_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve invoice-related tasks."""
        logger.info("Solving invoice task")
        # TODO: Implement invoice task solving
        return {"created_objects": []}

    async def _solve_project_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve project-related tasks."""
        logger.info("Solving project task")
        # TODO: Implement project task solving
        return {"created_objects": []}

    async def _solve_travel_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve travel expense tasks."""
        logger.info("Solving travel expense task")
        # TODO: Implement travel expense task solving
        return {"created_objects": []}

    async def _solve_department_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve department tasks."""
        logger.info("Solving department task")
        # TODO: Implement department task solving
        return {"created_objects": []}
