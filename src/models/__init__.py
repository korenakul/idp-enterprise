"""
Models module for IDP Enterprise Document Intelligence Platform.
Pydantic schemas and data models for the document processing system.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum


class DocumentStatus(str, Enum):
    """Document processing status."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class DocumentType(str, Enum):
    """Supported document types."""
    INVOICE = "invoice"
    CONTRACT = "contract"
    RESUME = "resume"
    RECEIPT = "receipt"
    BANK_STATEMENT = "bank_statement"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver_license"
    MEDICAL_RECORD = "medical_record"
    FORM = "form"
    GENERAL_DOCUMENT = "general_document"


class ExtractedData(BaseModel):
    """Extracted information from document."""
    field_name: str = Field(..., description="Name of the extracted field")
    value: Any = Field(..., description="Extracted value")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence score")


class DocumentResponse(BaseModel):
    """Document processing response."""
    document_id: str = Field(..., description="Unique document identifier")
    filename: str = Field(..., description="Original filename")
    status: DocumentStatus = Field(..., description="Processing status")
    document_type: Optional[DocumentType] = Field(None, description="Detected document type")
    confidence: float = Field(0.0, ge=0.0, le=1.0, description="Confidence score")
    extracted_data: Optional[Dict[str, Any]] = Field(None, description="Extracted information")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = Field(None, description="Processing completion time")


class DocumentUploadResponse(BaseModel):
    """Document upload response."""
    status: str = Field("success")
    document_id: str = Field(..., description="Generated document ID")
    filename: str = Field(..., description="Uploaded filename")
    message: Optional[str] = Field(None, description="Additional message")


class BatchRequest(BaseModel):
    """Batch processing request."""
    files: List[str] = Field(..., description="List of file paths or URLs")
    document_type: Optional[DocumentType] = Field(None, description="Document type override")


class BatchResponse(BaseModel):
    """Batch processing response."""
    batch_id: str = Field(..., description="Unique batch identifier")
    total_count: int = Field(..., description="Total files in batch")
    success_count: int = Field(..., description="Successfully processed count")
    failed_count: int = Field(..., description="Failed count")
    results: List[Dict[str, Any]] = Field(default_factory=list, description="Processing results")


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = Field("healthy")
    version: str = Field("2.0.0")
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    uptime_seconds: Optional[float] = Field(None)


class SearchQuery(BaseModel):
    """Document search query."""
    query: str = Field(..., description="Search query")
    document_type: Optional[DocumentType] = Field(None)
    limit: int = Field(10, ge=1, le=100)
    offset: int = Field(0, ge=0)


class SearchResponse(BaseModel):
    """Search results response."""
    total: int = Field(..., description="Total matching documents")
    results: List[DocumentResponse] = Field(default_factory=list)


class MetricsResponse(BaseModel):
    """System metrics response."""
    documents_processed: int = Field(0, description="Total documents processed")
    avg_response_time: float = Field(0.0, description="Average response time in seconds")
    active_workers: int = Field(0, description="Active processing workers")
    queue_length: int = Field(0, description="Pending tasks in queue")
    error_rate: float = Field(0.0, ge=0.0, le=1.0, description="Error rate")


__all__ = [
    'DocumentStatus',
    'DocumentType',
    'ExtractedData',
    'DocumentResponse',
    'DocumentUploadResponse',
    'BatchRequest',
    'BatchResponse',
    'HealthResponse',
    'SearchQuery',
    'SearchResponse',
    'MetricsResponse'
]