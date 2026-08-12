"""
Database models for IDP Enterprise Document Intelligence Platform.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Document(Base):
    """Document processing record."""
    
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String(255), unique=True, nullable=False, index=True)
    filename = Column(String(512), nullable=False)
    original_path = Column(Text)
    file_type = Column(String(50))
    file_size = Column(Integer)
    document_type = Column(String(100))
    status = Column(String(50), default='pending')
    result_data = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime)
    error = Column(Text)
    
    def to_dict(self):
        return {
            'document_id': self.document_id,
            'filename': self.filename,
            'original_path': self.original_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'document_type': self.document_type,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }


class DocumentVersion(Base):
    """Document version tracking."""
    
    __tablename__ = 'document_versions'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String(255), index=True)
    version = Column(Integer, default=1)
    ocr_text = Column(Text)
    extracted_data = Column(JSON)
    confidence = Column(Float)
    engine_used = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)


class ProcessingLog(Base):
    """Processing workflow logs."""
    
    __tablename__ = 'processing_logs'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String(255), index=True)
    step = Column(String(100))
    status = Column(String(50))
    details = Column(Text)
    duration_ms = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)


class AuditLog(Base):
    """Audit trail for document operations."""
    
    __tablename__ = 'audit_logs'
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String(255), index=True)
    action = Column(String(100))
    user = Column(String(255))
    details = Column(Text)
    ip_address = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
