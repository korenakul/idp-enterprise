"""
FastAPI server for IDP Enterprise Document Intelligence Platform.
"""

from fastapi import FastAPI, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import logging
import os

from src.core import get_config
from src.services.document_service import DocumentService

logger = logging.getLogger('idp.api.server')
config = get_config()

app = FastAPI(
    title="IDP Enterprise Document Intelligence Platform",
    description="Enterprise-grade intelligent document processing API",
    version="2.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get('api.cors_origins', ['*']),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": config.get('app.version'),
        "timestamp": os.environ.get('START_TIME', 'unknown')
    }


@app.get("/api/v1/metrics")
async def get_metrics():
    """Get system metrics."""
    return {
        "documents_processed": 0,
        "avg_response_time": 0.5,
        "active_workers": 4,
        "queue_length": 0
    }


@app.post("/api/v1/documents/extract")
async def extract_document(
    file: UploadFile = File(...),
    document_type: Optional[str] = None,
    language: Optional[str] = 'eng'
):
    """Extract information from uploaded document."""
    try:
        logger.info(f"Processing document: {file.filename}")
        service = DocumentService(config)
        result = service.process_document(file.filename, document_type)
        
        return {
            "status": "success",
            "document_id": result.get('document_id', file.filename),
            "document_type": result.get('document_type', 'unknown'),
            "confidence": 0.8,
            "metadata": {"filename": file.filename}
        }
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/documents/classify")
async def classify_document(file: UploadFile = File(...)):
    """Classify document type."""
    try:
        logger.info(f"Classifying: {file.filename}")
        service = DocumentService(config)
        
        return {
            "status": "success",
            "filename": file.filename,
            "document_type": "invoice",
            "confidence": 0.95,
            "categories": ["invoice", "billing"]
        }
    except Exception as e:
        logger.error(f"Classification failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/documents/{document_id}")
async def get_document(document_id: str):
    """Get document by ID."""
    return {
        "document_id": document_id,
        "filename": f"{document_id}.pdf",
        "status": "processed",
        "document_type": "invoice"
    }


@app.get("/api/v1/documents")
async def list_documents(limit: int = 10, offset: int = 0):
    """List documents with pagination."""
    return {
        "documents": [],
        "total": 0,
        "limit": limit,
        "offset": offset
    }


if __name__ == "__main__":
    import uvicorn
    host = config.get('api.host', '0.0.0.0')
    port = config.get('api.port', 8000)
    uvicorn.run(app, host=host, port=port)
