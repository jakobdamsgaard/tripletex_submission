"""Pydantic models for API request/response handling."""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


# ============================================================================
# Request Models
# ============================================================================

class TripletexCredentials(BaseModel):
    """Tripletex authentication credentials."""

    api_url: Optional[str] = None
    session_token: Optional[str] = None
    company_id: str = "0"


class TaskRequest(BaseModel):
    """Incoming task request to /solve endpoint."""

    task_prompt: str
    language: str = "en"
    attachments: Optional[List[str]] = None
    tripletex: Optional[TripletexCredentials] = None


# ============================================================================
# Response Models
# ============================================================================

class TaskResult(BaseModel):
    """Result of task execution."""

    created_objects: Optional[List[Dict[str, Any]]] = None
    updated_objects: Optional[List[Dict[str, Any]]] = None
    deleted_objects: Optional[List[Dict[str, Any]]] = None
    api_calls: int = 0
    execution_time_ms: int = 0
    success: bool = True
    message: Optional[str] = None


class TaskResponse(BaseModel):
    """Response to submit endpoint."""

    status: str  # "completed", "failed"
    result: Optional[TaskResult] = None
    error: Optional[str] = None


# ============================================================================
# Tripletex Domain Models
# ============================================================================

class Employee(BaseModel):
    """Employee entity in Tripletex."""

    id: Optional[int] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    department: Optional[Dict[str, Any]] = None
    roles: Optional[List[Dict[str, Any]]] = None
    version: Optional[int] = None


class Customer(BaseModel):
    """Customer entity in Tripletex."""

    id: Optional[int] = None
    name: str
    organizationNumber: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    invoiceEmail: Optional[str] = None
    version: Optional[int] = None


class Product(BaseModel):
    """Product entity in Tripletex."""

    id: Optional[int] = None
    number: Optional[str] = None
    name: str
    unit: Optional[str] = None
    costPrice: Optional[float] = None
    sellingPrice: Optional[float] = None
    version: Optional[int] = None


class Invoice(BaseModel):
    """Invoice entity in Tripletex."""

    id: Optional[int] = None
    invoiceNumber: Optional[int] = None
    customer: Optional[Dict[str, Any]] = None
    invoiceDate: Optional[str] = None  # YYYY-MM-DD
    dueDate: Optional[str] = None  # YYYY-MM-DD
    amount: Optional[float] = None
    status: Optional[str] = None
    lines: Optional[List[Dict[str, Any]]] = None
    version: Optional[int] = None


class Project(BaseModel):
    """Project entity in Tripletex."""

    id: Optional[int] = None
    name: str
    customer: Optional[Dict[str, Any]] = None
    startDate: Optional[str] = None  # YYYY-MM-DD
    endDate: Optional[str] = None  # YYYY-MM-DD
    budget: Optional[float] = None
    version: Optional[int] = None


class Department(BaseModel):
    """Department entity in Tripletex."""

    id: Optional[int] = None
    name: str
    number: Optional[str] = None
    version: Optional[int] = None


class TravelExpense(BaseModel):
    """Travel expense entity in Tripletex."""

    id: Optional[int] = None
    employee: Optional[Dict[str, Any]] = None
    department: Optional[Dict[str, Any]] = None
    purpose: Optional[str] = None
    startDate: Optional[str] = None  # YYYY-MM-DD
    endDate: Optional[str] = None  # YYYY-MM-DD
    status: Optional[str] = None
    version: Optional[int] = None


# ============================================================================
# API Response Models
# ============================================================================

class APIResponseEnvelope(BaseModel):
    """Generic API response envelope from Tripletex."""
    model_config = ConfigDict(extra="allow")

    fullResultSize: Optional[int] = None
    from_: Optional[int] = Field(None, alias="from")
    count: Optional[int] = None
    versionDigest: Optional[str] = None
    values: Optional[List[Dict[str, Any]]] = None


class SingleValueEnvelope(BaseModel):
    """Single value response envelope."""
    model_config = ConfigDict(extra="allow")

    value: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseModel):
    """Error response from Tripletex API."""

    status: int
    code: int
    message: str
    link: Optional[str] = None
    developerMessage: Optional[str] = None
    validationMessages: Optional[List[Dict[str, str]]] = None
    requestId: Optional[str] = None
