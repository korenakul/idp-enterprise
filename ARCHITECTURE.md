# IDP Enterprise Document Intelligence Platform - Architecture Documentation

## Overview

This document provides detailed technical architecture information for the IDP Enterprise Document Intelligence Platform.

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         Frontend Layer                                   │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │   Web UI    │  │   CLI Tool  │  │ Mobile App  │  │ Third-party  │   │
│  │  (React/Vue)│  │ (Python)    │  │  (iOS/Android)│  │ Integrations │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘   │
│         │                 │                 │                 │          │
│         └─────────────────┴─────────────────┴─────────────────┘          │
│                           │                                              │
│                   ┌───────▼───────┐                                      │
│                   │   API Layer   │                                      │
│                   │   (FastAPI)   │                                      │
│                   └───────┬───────┘                                      │
└───────────────────────────┼──────────────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────────────┐
│                    Business Logic Layer                                  │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │  Processor  │  │  Classifier │  │  Extractor  │  │  Workflow    │   │
│  │   Engine    │  │  & ML Models│  │ & Templates │  │   Engine     │   │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬───────┘   │
│         │                 │                 │                 │          │
│         └─────────────────┴─────────────────┴─────────────────┘          │
│                           │                                              │
│                   ┌───────▼───────┐                                      │
│                   │ Integration   │                                      │
│                   │   Layer       │                                      │
│                   └───────┬───────┘                                      │
│                  ┌────────▼────────┐                                     │
│  ┌─────────────┐ ┌───────┬───────┐ ┌───────▼────────┐                  │
│  │    ERP      │ │   CRM     │ │  Database (SQL)  │                  │
│  │  (SAP, etc) │ │ (Salesforce)│ │  (PostgreSQL)  │                  │
│  └─────────────┘ └───────────┘ └──────────────────┘                  │
│  ┌─────────────┐ ┌───────┬───────┐ ┌───────▼────────┐                  │
│  │   Queue     │ │   Redis   │ │    Cache         │                  │
│  │  (Celery)   │ │           │ │  (Redis)         │                  │
│  └─────────────┘ └───────────┘ └──────────────────┘                  │
└──────────────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼──────────────────────────────────────────────┐
│                        Data Layer                                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐   │
│  │  Documents  │  │  Processed  │  │   Metadata  │  │    Logs      │   │
│  │   Storage   │  │  Documents  │  │  (Database) │  │  (Elastic)   │   │
│  └─────────────┘  └─────────────┘  └─────────────┘  └──────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Core Module (`src/core/`)

#### Configuration Management (`config.py`)

```python
class ConfigManager:
    """Centralized configuration management."""
    
    def _load_config(self, config_path):
        """Load configuration from file with defaults."""
        defaults = {
            'app': {...},
            'paths': {...},
            'ocr': {...},
            'ai': {...}
        }
        # Merge user config with defaults
        if config_path:
            user_config = safe_json_load(config_path, {})
            self._merge_config(defaults, user_config)
        return defaults
```

**Key Features:**
- Hierarchical configuration loading
- Environment variable support
- Config file merging
- Validation on load

### 2. ML Module (`src/ml/`)

#### OCR Engine Architecture

```
BaseOCREngine
    ├── TesseractEngine (Local, Open Source)
    ├── GeminiEngine (Google Cloud)
    ├── AWSlextractEngine (AWS Textract)
    ├── AzureOCREngine (Azure Form Recognizer)
    └── GoogleVisionEngine (Google Vision API)
```

**Engine Selection Strategy:**
1. Try primary engine (default: Tesseract)
2. If confidence < threshold, try secondary engine
3. Aggregate results with weighted confidence
4. Return best result

#### Document Classification

```python
class DocumentClassifier:
    """ML-based document classification."""
    
    def __init__(self, config):
        self.model = pipeline(
            'text-classification',
            model=config.get('classification_model')
        )
    
    def classify(self, text):
        """Classify document type."""
        if self.model:
            return self._ml_classify(text)
        else:
            return self._keyword_classify(text)
```

**Classification Categories:**
- Invoice (billing, payment)
- Contract (agreements, legal)
- Resume (CV, job application)
- Medical Record (healthcare)
- Bank Statement (financial)
- Passport (identity)
- Driver License (identity)
- Form (generic forms)

#### Information Extraction

```python
class InformationExtractor:
    """Template-based and ML-based extraction."""
    
    def __init__(self, config):
        self.rules = {
            'invoice': {...},
            'contract': {...},
            # ... more rules
        }
    
    def extract(self, text, doc_type):
        """Extract information using rules."""
        if doc_type in self.rules:
            return self._extract_with_rules(text, doc_type)
        return self._extract_generic(text)
```

**Extraction Patterns:**
- Invoice Number
- Date
- Amount
- Vendor
- Customer
- Email
- Phone
- URLs

### 3. Services Module (`src/services/`)

#### DocumentService

**Workflow:**
1. Load document
2. Validate file format
3. Extract metadata
4. Process document (OCR + Classification + Extraction)
5. Store results
6. Return output

```python
def process_document(self, document_path, document_type=None):
    """Process a single document."""
    path = Path(document_path)
    doc_id = f"doc_{path.stem}_{timestamp}"
    
    result = {
        'document_id': doc_id,
        'status': 'processing',
        'metadata': {...},
        'extracted_data': {...}
    }
    
    # Determine document type
    result['metadata']['document_type'] = \
        document_type or self._classify_document(path)
    
    result['status'] = 'completed'
    self._save_result(result)
    
    return result
```

### 4. Workers Module (`src/workers/`)

#### DocumentProcessor

**Background Processing:**
- Queue-based processing
- Retry logic with exponential backoff
- Progress tracking
- Metrics collection

```python
class DocumentProcessor:
    """Background document processor."""
    
    def __init__(self, config):
        self.config = config
        self.ocr_engines = config.get('ocr.engines')
        self.metrics = {...}
    
    def process(self, document_path, document_type=None):
        """Process document with all OCR engines."""
        result = {'document_id': doc_id, 'status': 'pending'}
        
        for engine_name in self.ocr_engines:
            engine_result = self._process_with_engine(
                document_path, engine_name
            )
            result['ocr_results'].append(engine_result)
            if engine_result.get('success'):
                break  # Use first successful engine
        
        result['status'] = 'completed'
        return result
```

### 5. Database Module (`src/database/`)

#### Models

```python
class Document(Base):
    """Document processing record."""
    
    id = Column(Integer, primary_key=True)
    document_id = Column(String, unique=True, index=True)
    filename = Column(String)
    original_path = Column(Text)
    file_type = Column(String)
    file_size = Column(Integer)
    document_type = Column(String)
    status = Column(String, default='pending')
    result_data = Column(JSON)
    created_at = Column(DateTime)
    processed_at = Column(DateTime)
    error = Column(Text)
```

#### DatabaseManager

```python
class DatabaseManager:
    """Manage database connections."""
    
    def __init__(self, config):
        self.config = config
        self._engine = None
        self._session = None
    
    @contextmanager
    def session_scope(self):
        """Provide transaction scope."""
        session = self._session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
```

### 6. API Module (`src/api/`)

#### FastAPI Server

**Endpoints:**
- `GET /api/v1/health` - Health check
- `GET /api/v1/metrics` - System metrics
- `POST /api/v1/documents/extract` - Extract from document
- `POST /api/v1/documents/classify` - Classify document type
- `GET /api/v1/documents/{id}` - Get document
- `GET /api/v1/documents` - List documents

**CORS Configuration:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.get('api.cors_origins', ['*']),
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

### 7. Integrations Module (`src/integrations/`)

#### ERP Connectors

```python
class SAPConnector(ERPConnector):
    """SAP ERP connector."""
    
    def submit_invoice(self, invoice):
        """Submit invoice to SAP."""
        return {
            'status': 'success',
            'document_type': 'invoice',
            'erp_id': 'SAP-' + invoice.get('invoice_number')
        }
```

Supported ERP Systems:
- SAP ECC/ERP
- Oracle ERP Cloud
- Microsoft Dynamics

#### CRM Connectors

```python
class SalesforceConnector(CRMConnector):
    """Salesforce CRM connector."""
    
    def create_opportunity(self, invoice):
        """Create opportunity in Salesforce."""
        return {
            'status': 'success',
            'opportunity_id': 'SF-' + invoice.get('invoice_number')
        }
```

Supported CRM Systems:
- Salesforce
- HubSpot
- Microsoft Dynamics CRM

## Data Flow

### Document Processing Pipeline

```
Document Input
    ↓
Preprocessing (Image optimization)
    ↓
OCR Extraction (Tesseract/Gemini/AWS)
    ↓
Text Cleaning & Normalization
    ↓
Document Classification (ML Model)
    ↓
Template Selection (based on type)
    ↓
Information Extraction (Rules + ML)
    ↓
Data Validation & Enrichment
    ↓
Integration (ERP/CRM/Database)
    ↓
Result Storage
    ↓
Response Generation
```

### Batch Processing Pipeline

```
Batch Queue
    ↓
Job Splitter
    ↓
Worker Pool
    ├── Worker 1 → Document 1
    ├── Worker 2 → Document 2
    ├── Worker 3 → Document 3
    └── Worker 4 → Document 4
    ↓
Result Aggregator
    ↓
Summary Generation
    ↓
Notification (Email/Webhook)
```

## Security Architecture

### Authentication
- JWT tokens (ready for implementation)
- API key authentication
- OAuth 2.0 support (ready)

### Authorization
- Role-based access control (RBAC)
- Document-level permissions
- Audit logging

### Data Protection
- Encryption at rest (database)
- Encryption in transit (HTTPS)
- Secure file handling
- Input validation

## Performance Considerations

### Scaling Strategies

**Vertical Scaling:**
- Increase CPU/RAM
- Add more OCR engines
- Optimize database queries

**Horizontal Scaling:**
- Add worker nodes
- Load balancing for API
- Distributed processing

### Caching
- Redis for session caching
- File system caching for processed documents
- Model caching (ML models loaded once)

### Optimization Techniques
- Batch processing for multiple documents
- Parallel OCR processing
- Lazy loading of ML models
- Connection pooling for database

## Error Handling

### Error Types
1. Input Validation Errors
2. OCR Processing Errors
3. Integration Errors
4. System Errors

### Retry Strategy
- Exponential backoff
- Maximum retry count
- Dead letter queue for failed jobs

### Monitoring
- Error rate tracking
- Alerting on high error rates
- Error logging and analysis
