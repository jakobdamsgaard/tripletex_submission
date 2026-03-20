"""Main task solver orchestrator."""

import logging
import time
from typing import Dict, Any, Optional
from src.api.client import TripletexClient, APIError
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
        _ = attachments

        # Route to the primary task entity, not referenced entities inside the prompt.
        if "delete" in intent:
            return await self._solve_correction_task(prompt, task_info)
        elif "invoice" in intent:
            return await self._solve_invoice_task(prompt, task_info)
        elif "project" in intent:
            return await self._solve_project_task(prompt, task_info)
        elif "travel" in intent:
            return await self._solve_travel_task(prompt, task_info)
        elif "department" in intent:
            return await self._solve_department_task(prompt, task_info)
        elif "product" in intent:
            return await self._solve_product_task(prompt, task_info)
        elif "employee" in intent:
            return await self._solve_employee_task(prompt, task_info)
        elif "customer" in intent:
            return await self._solve_customer_task(prompt, task_info)
        else:
            logger.warning(f"Unknown task intent: {intent}")
            raise ValueError(f"Unsupported task intent: {intent}")

    async def _solve_employee_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve employee-related tasks."""
        logger.info("Solving employee task")
        entities = task_info.get("entities", {})
        intent = task_info.get("intent", "")

        if "update" in intent:
            employee_id = entities.get("employee_id")
            if not employee_id:
                raise ValueError("Could not extract employee ID for update task")

            payload: Dict[str, Any] = {}
            if entities.get("email"):
                payload["email"] = entities["email"]
            if entities.get("phone"):
                payload["phone"] = entities["phone"]
            if entities.get("department_id"):
                payload["department"] = {"id": entities["department_id"]}

            if not payload:
                raise ValueError("No supported employee fields found to update")

            response = await self._put(f"/employee/{employee_id}", payload)
            return {"updated_objects": [self._unwrap_response(response)]}

        employee_name = entities.get("employee_name")
        if not employee_name:
            raise ValueError("Could not extract employee name from task prompt")

        payload: Dict[str, Any] = {
            "firstName": employee_name["first_name"],
            "lastName": employee_name["last_name"],
        }
        if entities.get("email"):
            payload["email"] = entities["email"]
        if entities.get("phone"):
            payload["phone"] = entities["phone"]

        response = await self._post("/employee", payload)
        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_customer_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve customer-related tasks."""
        logger.info("Solving customer task")
        entities = task_info.get("entities", {})
        intent = task_info.get("intent", "")

        if "update" in intent:
            customer_id = entities.get("customer_id")
            if not customer_id:
                raise ValueError("Could not extract customer ID for update task")

            payload: Dict[str, Any] = {}
            if entities.get("email"):
                payload["email"] = entities["email"]
            if entities.get("phone"):
                payload["phone"] = entities["phone"]

            if not payload:
                raise ValueError("No supported customer fields found to update")

            response = await self._put(f"/customer/{customer_id}", payload)
            return {"updated_objects": [self._unwrap_response(response)]}

        customer_name = entities.get("customer_name")

        if not customer_name:
            names = entities.get("names") or []
            customer_name = " ".join(names).strip() if names else None

        if not customer_name:
            raise ValueError("Could not extract customer name from task prompt")

        payload = {"name": customer_name}
        if entities.get("organization_number"):
            payload["organizationNumber"] = entities["organization_number"]
        if entities.get("email"):
            payload["email"] = entities["email"]
        if entities.get("phone"):
            payload["phone"] = entities["phone"]

        response = await self._post("/customer", payload)
        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_invoice_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve invoice-related tasks."""
        logger.info("Solving invoice task")
        entities = task_info.get("entities", {})
        intent = task_info.get("intent", "")

        if "payment" in intent:
            invoice_id = entities.get("invoice_id")
            amount = entities.get("amount")
            payment_date = entities.get("payment_date")
            if not invoice_id or amount is None or not payment_date:
                raise ValueError("Could not extract invoice payment details from task prompt")

            payload = {
                "amount": amount,
                "paymentDate": payment_date,
            }
            response = await self._post(f"/invoice/{invoice_id}/payment", payload)
            return {"updated_objects": [self._unwrap_response(response)]}

        customer_id = entities.get("customer_id")
        invoice_date = entities.get("invoice_date")
        lines = entities.get("invoice_lines") or []
        if not customer_id or not invoice_date or not lines:
            raise ValueError("Could not extract invoice customer, date, and lines from task prompt")

        payload: Dict[str, Any] = {
            "customer": {"id": customer_id},
            "invoiceDate": invoice_date,
            "lines": lines,
        }
        if entities.get("due_date"):
            payload["dueDate"] = entities["due_date"]

        response = await self._post("/invoice", payload)
        invoice_response = self._unwrap_response(response)
        created_objects = [invoice_response]

        if entities.get("should_post_invoice"):
            invoice_id = invoice_response.get("id")
            if invoice_id is not None:
                posted_response = await self._post(f"/invoice/{invoice_id}/:post", {})
                created_objects.append(self._unwrap_response(posted_response))

        return {"created_objects": created_objects}

    async def _solve_project_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve project-related tasks."""
        logger.info("Solving project task")
        entities = task_info.get("entities", {})
        if entities.get("is_project_participant_task"):
            project_id = entities.get("project_id")
            employee_id = entities.get("employee_id")
            if not project_id or not employee_id:
                raise ValueError("Could not extract project ID and employee ID for participant task")

            response = await self._post(
                f"/project/{project_id}/participant",
                {"employee": {"id": employee_id}},
            )
            return {"updated_objects": [self._unwrap_response(response)]}

        project_name = entities.get("project_name")

        if not project_name:
            raise ValueError("Could not extract project name from task prompt")

        payload: Dict[str, Any] = {"name": project_name}
        customer_id = entities.get("customer_id")
        if customer_id:
            payload["customer"] = {"id": customer_id}
        if entities.get("start_date"):
            payload["startDate"] = entities["start_date"]
        if entities.get("end_date"):
            payload["endDate"] = entities["end_date"]

        response = await self._post("/project", payload)
        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_travel_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve travel expense tasks."""
        logger.info("Solving travel expense task")
        entities = task_info.get("entities", {})
        employee_id = entities.get("employee_id")
        start_date = entities.get("start_date")

        if not employee_id or not start_date:
            raise ValueError("Could not extract employee ID and start date from travel task")

        payload: Dict[str, Any] = {
            "employee": {"id": employee_id},
            "startDate": start_date,
        }
        if entities.get("end_date"):
            payload["endDate"] = entities["end_date"]
        if entities.get("purpose"):
            payload["purpose"] = entities["purpose"]

        response = await self._post("/travelExpense", payload)
        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_department_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve department tasks."""
        logger.info("Solving department task")
        entities = task_info.get("entities", {})
        department_name = entities.get("department_name")

        if not department_name:
            raise ValueError("Could not extract department name from task prompt")

        payload: Dict[str, Any] = {"name": department_name}
        if entities.get("department_number"):
            payload["number"] = entities["department_number"]

        try:
            response = await self._post("/department", payload)
        except ValueError as exc:
            if "number" in payload and "number" in str(exc):
                logger.info("Retrying department creation without unsupported 'number' field")
                fallback_payload = {"name": department_name}
                response = await self._post("/department", fallback_payload)
            else:
                raise

        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_product_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Solve product-related tasks."""
        logger.info("Solving product task")
        entities = task_info.get("entities", {})
        product_name = entities.get("product_name")
        if not product_name:
            raise ValueError("Could not extract product name from task prompt")

        payload: Dict[str, Any] = {"name": product_name}
        amount = entities.get("amount")
        if amount is not None:
            payload["sellingPrice"] = amount

        response = await self._post("/product", payload)
        return {"created_objects": [self._unwrap_response(response)]}

    async def _solve_correction_task(self, prompt: str, task_info: Dict[str, Any]) -> Dict[str, Any]:
        """Handle simple delete flows."""
        logger.info("Solving correction task")
        entities = task_info.get("entities", {})
        intent = task_info.get("intent", "")

        if "customer" in intent and entities.get("customer_id"):
            deleted_id = entities["customer_id"]
            await self._delete(f"/customer/{deleted_id}")
            return {"deleted_objects": [{"id": deleted_id, "type": "customer"}]}

        if "employee" in intent and entities.get("employee_id"):
            deleted_id = entities["employee_id"]
            await self._delete(f"/employee/{deleted_id}")
            return {"deleted_objects": [{"id": deleted_id, "type": "employee"}]}

        if "invoice" in intent and entities.get("invoice_id"):
            deleted_id = entities["invoice_id"]
            await self._delete(f"/invoice/{deleted_id}")
            return {"deleted_objects": [{"id": deleted_id, "type": "invoice"}]}

        if "travel" in intent and entities.get("travel_expense_id"):
            deleted_id = entities["travel_expense_id"]
            await self._delete(f"/travelExpense/{deleted_id}")
            return {"deleted_objects": [{"id": deleted_id, "type": "travelExpense"}]}

        raise ValueError(f"Delete task not supported for prompt: {prompt}")

    async def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST wrapper that counts attempted API calls and enriches errors."""
        self.api_calls += 1
        try:
            return await self.client.post(endpoint, payload)
        except APIError as exc:
            raise ValueError(self._format_api_error(exc)) from exc

    async def _delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE wrapper that counts attempted API calls and enriches errors."""
        self.api_calls += 1
        try:
            return await self.client.delete(endpoint)
        except APIError as exc:
            raise ValueError(self._format_api_error(exc)) from exc

    async def _put(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """PUT wrapper that counts attempted API calls and enriches errors."""
        self.api_calls += 1
        try:
            return await self.client.put(endpoint, payload)
        except APIError as exc:
            raise ValueError(self._format_api_error(exc)) from exc

    @staticmethod
    def _unwrap_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Tripletex single-value responses."""
        return response.get("value", response)

    async def _get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """GET wrapper that counts attempted API calls and enriches errors."""
        self.api_calls += 1
        try:
            return await self.client.get(endpoint, params=params)
        except APIError as exc:
            raise ValueError(self._format_api_error(exc)) from exc

    async def _get_default_employee_id(self) -> Optional[int]:
        """Fetch a fallback employee ID for flows that require one."""
        response = await self._get("/employee", params={"count": 1})
        employees = response.get("values") or []
        if not employees:
            return None

        employee_id = employees[0].get("id")
        return int(employee_id) if employee_id is not None else None

    @staticmethod
    def _format_api_error(exc: APIError) -> str:
        """Convert Tripletex API errors into a short readable message."""
        details = []
        for validation in exc.validation_messages or []:
            field = validation.get("field", "field")
            message = validation.get("message", "invalid value")
            details.append(f"{field}: {message}")

        if details:
            return f"{exc.message} ({'; '.join(details)})"

        return exc.message
