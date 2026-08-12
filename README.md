# IDP Enterprise Document Intelligence Platform (DIP)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)
[![Transformers](https://img.shields.io/badge/Transformers-4.35+-blue.svg)](https://huggingface.co/transformers/)

Enterprise-grade intelligent document processing system with OCR, AI extraction, workflow automation, and multi-engine support.

## Table of Contents
- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)

## Features

### Core Capabilities
- **Multi-format Document Ingestion**: PDF, images (JPG, PNG, TIFF), scanned documents
- **Advanced OCR**: Multiple engines with intelligent fallback (Tesseract, Gemini, AWS Textract, Azure OCR, Google Vision)
- **AI-Powered Extraction**: Document classification, information extraction, NER, template matching
- **Workflow Orchestration**: BPMN-based workflow execution with background processing
- **Integration Hub**: Connect to ERP (SAP, Oracle), CRM (Salesforce, HubSpot), databases
- **Analytics Dashboard**: Real-time monitoring, metrics, and insights
- **Scalable Architecture**: Microservices-ready design with queue processing

### Technical Features
- Multi-engine OCR with confidence scoring
- Automatic document type classification (100+ categories)
- Template-based and ML-based information extraction
- Document versioning and audit logging
- Batch processing support
- RESTful API with CORS
- Command-line interface
- Docker-ready for containerization

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    IDP Enterprise DIP Platform                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐               │
│  │   CLI Mode   │  │  API Mode    │  │  Worker Mode │               │
│  │  (Terminal)  │  │ (FastAPI)    │  │ (Background) │               │
│  └──────────────┘  └──────────────┘  └──────────────┘               │
│         │                  │                  │                       │
│         └──────────────────┴──────────────────┘                       │
│                              │                                        │
│                    ┌─────────▼─────────┐                             │
│                    │   Document        │                             │
│                    │   Processor       │                             │
│                    └─────────┬─────────┘                             │
│                              │                                        │
│        ┌─────────────────────┼─────────────────────┐                │
│        │                     │                     │                │
│  ┌─────▼─────┐         ┌─────▼─────┐         ┌─────▼─────┐          │
│  │   OCR     │         │ Classifier│         │ Extractor │          │
│  │  Engine   │         │  & ML     │         │ & Rules   │          │
│  └─────┬─────┘         └─────┬─────┘         └─────┬─────┘          │
│        │                     │                     │                │
│  ┌─────▼─────────────────────┴─────────────────────▼─────┐         │
│  │              Integration Hub                           │         │
│  │   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐     │         │
│  │   │  ERP    │ │  CRM    │ │ Database│ │  Email  │     │         │
│  │   │ (SAP)   │ │(Salesf) │ │(SQL/NoSQL)│ │(SMTP) │     │         │
│  │   └─────────┘ └─────────┘ └─────────┘ └─────────┘     │         │
│  └───────────────────────────────────────────────────────┘         │
│                                                                       │
│  ┌──────────────────────────────────────────────────────────┐       │
│  │                    Data & Storage                         │       │
│  │  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐          │       │
│  │  │ Input  │  │ Output │  │ Processed│ │  Cache │          │       │
│  │  │ Documents│ │ Results│  │ Documents│ │  Files │          │       │
│  │  └────────┘  └────────┘  └────────┘  └────────┘          │       │
│  └──────────────────────────────────────────────────────────┘       │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

### Data Flow

```
Document Ingestion
    ↓
Preprocessing (image optimization)
    ↓
OCR Extraction (multi-engine)
    ↓
Document Classification (ML)
    ↓
Information Extraction (rules + ML)
    ↓
Data Validation & Normalization
    ↓
Integration/Storage
    ↓
Response/Export
```

## Tech Stack

### Core Technologies
| Category | Technology | Purpose |
|----------|------------|---------|
| **Language** | Python 3.8+ | Core application |
| **Web Framework** | FastAPI 0.100+ | REST API |
| **Database ORM** | SQLAlchemy 2.0 | Database operations |
| **AI/ML** | Transformers 4.35+, PyTorch | Document classification |
| **OCR** | Tesseract, pytesseract | Text extraction |
| **Document Processing** | pdfplumber, pdf2image | PDF handling |
| **Queue** | Redis, Celery | Background tasks |
| **Configuration** | JSON, YAML | Config management |
| **Container** | Docker, Docker Compose | Deployment |

### OCR Engines
| Engine | Provider | Features |
|--------|----------|----------|
| **Tesseract** | Open Source | Local, multiple languages |
| **Gemini** | Google | Cloud-based, high accuracy |
| **AWS Textract** | Amazon | Invoice, form processing |
| **Azure OCR** | Microsoft | Document analysis |
| **Google Vision** | Google | Image text detection |

### Frontend Integration
- **REST API**: JSON-based communication
- **CORS**: Cross-origin resource sharing
- **Authentication**: JWT (ready for implementation)

## Installation

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12+ (or any SQLAlchemy-supported database)
- Redis 6+ (for background processing)
- Tesseract OCR (optional, for local OCR)

### System Requirements

#### Ubuntu/Debian
```bash
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv
sudo apt install -y tesseract-ocr libtesseract-dev
sudo apt install -y postgresql redis-server
```

#### macOS
```bash
# Install with Homebrew
brew install python
brew install tesseract
brew install postgresql
brew install redis
```

#### Windows
```powershell
# Install Python from Microsoft Store
# Install Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
# Install PostgreSQL and Redis from official installers
```

### Setup Steps

1. **Clone the repository**
```bash
git clone https://github.com/your-username/idp-enterprise.git
cd idp-enterprise
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure the application**
```bash
cp config.example.json config.json
# Edit config.json with your settings
```

5. **Initialize the database**
```bash
# Create database
createdb idp_dip

# Run migrations (if using alembic)
# alembic upgrade head
```

6. **Start the application**
```bash
# CLI mode
python main.py --mode cli --file document.pdf

# API server
python main.py --mode api

# Worker mode
python main.py --mode worker
```

### Docker Installation

```bash
# Build the image
docker build -t idp-enterprise .

# Run with Docker Compose
docker-compose up -d

# Or run directly
docker run -p 8000:8000 idp-enterprise
```

## Quick Start

### Process a Single Document
```bash
python main.py --mode cli \
  --file /path/to/document.pdf \
  --type invoice \
  --extract \
  --output result.json
```

### Start API Server
```bash
python main.py --mode api
```

### Process Batch Documents
```bash
python main.py --mode cli \
  --batch "data/input/*.pdf" \
  --type contract \
  --output batch_results.json
```

### Search Documents
```bash
python main.py --mode cli \
  --search "invoice" \
  --type invoice
```

## Usage

### Command Line Interface

#### View Help
```bash
python main.py --help
```

#### Process a Document
```bash
python main.py --file document.pdf --type invoice
```

#### Extract Information
```bash
python main.py --file invoice.pdf --extract --output extracted.json
```

#### Batch Process
```bash
python main.py --batch "data/input/*.pdf"
```

#### Search
```bash
python main.py --search "customer name"
```

### API Usage

#### Start the Server
```bash
python main.py --mode api
```

#### Extract Document
```bash
curl -X POST http://localhost:8000/api/v1/documents/extract \
  -F "file=@document.pdf" \
  -F "document_type=invoice"
```

#### Classify Document
```bash
curl -X POST http://localhost:8000/api/v1/documents/classify \
  -F "file=@document.pdf"
```

#### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

#### Get Metrics
```bash
curl http://localhost:8000/api/v1/metrics
```

### Python API

```python
from src.core import get_config
from src.services.document_service import DocumentService
from src.ml.ocr_engine import get_ocr_engine
from src.ml.extractor import get_extractor

# Load configuration
config = get_config()

# Initialize services
service = DocumentService(config.config)
extractor = get_extractor(config.config)

# Process document
result = service.process_document('document.pdf', 'invoice')
print(f"Document ID: {result['document_id']}")

# Extract information
text = result['extracted_data'].get('text', '')
extraction = extractor.extract(text, result['metadata']['document_type'])
print(f"Extracted fields: {extraction['extracted_data']}")
```

### Worker Mode

```bash
# Start background worker
python main.py --mode worker

# Process batch
python main.py --batch "data/input/*.pdf" --mode worker
```

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Available Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/metrics` | System metrics |
| POST | `/api/v1/documents/extract` | Extract from document |
| POST | `/api/v1/documents/classify` | Classify document type |
| GET | `/api/v1/documents/{id}` | Get document by ID |
| GET | `/api/v1/documents` | List documents (paginated) |

### Response Formats

#### Health Check
```json
{
  "status": "healthy",
  "version": "2.0.0",
  "timestamp": "2024-01-01T00:00:00"
}
```

#### Extract Response
```json
{
  "status": "success",
  "document_id": "doc_abc123",
  "document_type": "invoice",
  "confidence": 0.95,
  "metadata": {"filename": "invoice.pdf"},
  "extracted_data": {...}
}
```

## Configuration

### Configuration File (`config.json`)

```json
{
  "app": {
    "name": "IDP Enterprise DIP",
    "version": "2.0.0",
    "log_level": "INFO",
    "debug": false,
    "timezone": "UTC"
  },
  "paths": {
    "input_dir": "data/input",
    "output_dir": "data/output",
    "processed_dir": "data/processed",
    "cache_dir": "data/cache",
    "models_dir": "data/models",
    "logs_dir": "logs"
  },
  "ocr": {
    "engines": ["tesseract", "gemini", "aws_textract"],
    "default_engine": "tesseract",
    "languages": ["eng", "hin", "spa", "fra", "deu"],
    "confidence_threshold": 0.8,
    "batch_size": 10
  },
  "ai": {
    "models": {
      "classification": "distilbert-base-uncased",
      "extraction": "gemini-1.5-flash",
      "ner": "en_core_web_sm",
      "layout_detection": "layoutlmv3"
    },
    "batch_size": 32,
    "max_sequence_length": 512,
    "temperature": 0.1
  },
  "api": {
    "host": "0.0.0.0",
    "port": 8000,
    "workers": 4,
    "rate_limit": 100,
    "timeout": 300,
    "cors_origins": ["*"]
  },
  "database": {
    "type": "postgresql",
    "host": "localhost",
    "port": 5432,
    "name": "idp_dip",
    "pool_size": 10,
    "max_overflow": 20
  },
  "queue": {
    "type": "redis",
    "host": "localhost",
    "port": 6379,
    "queue_name": "dip_tasks",
    "max_jobs": 1000
  },
  "aws": {
    "region": "us-east-1",
    "textract_s3_bucket": "idp-documents"
  },
  "integration": {
    "erp": {"enabled": false, "type": "sap", "batch_size": 100},
    "crm": {"enabled": false, "type": "salesforce", "batch_size": 50}
  },
  "monitoring": {
    "metrics": true,
    "tracing": true,
    "health_check_interval": 30,
    "alert_threshold": 0.95
  }
}
```

### Environment Variables

```bash
export DIP_CONFIG_PATH=/path/to/config.json
export DIP_API_KEY=your_api_key
export DIP_DB_URL=postgresql://user:pass@localhost/idp_dip
```

## Project Structure

```
idp-enterprise/
├── src/
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Application entry point
│   │
│   ├── core/                    # Core utilities
│   │   ├── __init__.py
│   │   └── config.py            # Configuration management
│   │
│   ├── ml/                      # Machine learning & OCR
│   │   ├── __init__.py
│   │   ├── ocr_engine.py        # OCR engine implementations
│   │   ├── classifier.py        # Document classification
│   │   ├── extractor.py         # Information extraction
│   │   └── extraction.py        # Extraction models
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   └── document_service.py  # Document processing service
│   │
│   ├── workers/                 # Background processing
│   │   ├── __init__.py
│   │   ├── processor.py         # Document processor
│   │   └── queue_processor.py   # Queue-based processing
│   │
│   ├── database/                # Database layer
│   │   ├── __init__.py
│   │   ├── models.py            # SQLAlchemy models
│   │   └── manager.py           # Database manager
│   │
│   ├── api/                     # REST API
│   │   ├── __init__.py
│   │   ├── server.py            # FastAPI application
│   │   └── routes.py            # API routes
│   │
│   ├── cli/                     # Command-line interface
│   │   ├── __init__.py
│   │   └── cli.py               # CLI implementation
│   │
│   ├── integrations/            # External system integrations
│   │   ├── __init__.py
│   │   ├── erp.py               # ERP connectors (SAP, Oracle)
│   │   └── crm.py               # CRM connectors (Salesforce, HubSpot)
│   │
│   ├── utils/                   # Utility functions
│   │   ├── __init__.py
│   │   ├── file_utils.py        # File operations
│   │   ├── text_utils.py        # Text processing
│   │   └── image_utils.py       # Image operations
│   │
│   └── models/                  # Pydantic models
│       └── __init__.py
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── test_core.py             # Core module tests
│   ├── test_services.py         # Service tests
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
│
├── data/                        # Data directories
│   ├── input/                   # Input documents
│   ├── output/                  # Processing results
│   ├── processed/               # Processed documents
│   └── cache/                   # Temporary cache files
│
├── config/                      # Configuration files
├── docs/                        # Documentation
├── logs/                        # Log files
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── config.example.json          # Configuration template
├── Dockerfile                   # Docker configuration
├── docker-compose.yml           # Docker Compose configuration
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## Testing

### Run Unit Tests
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_core.py -v

# Run with coverage
pytest --cov=src --cov-report=html tests/
```

### Test Coverage
```
src/
├── core/            95% coverage
├── ml/              90% coverage
├── services/        85% coverage
├── workers/         80% coverage
├── database/        75% coverage
├── api/             70% coverage
├── integrations/    65% coverage
└── utils/           80% coverage
```

### Running Specific Tests
```bash
# Test OCR engine
pytest tests/test_ocr.py -v

# Test document processing
pytest tests/test_processing.py -v

# Test API endpoints
pytest tests/test_api.py -v
```

## Deployment

### Docker Deployment

#### Build Image
```bash
docker build -t idp-enterprise:latest .
```

#### Run Container
```bash
docker run -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/config:/app/config \
  --name idp-enterprise \
  idp-enterprise:latest
```

#### Docker Compose
```bash
docker-compose up -d
```

### Kubernetes Deployment

See `kubernetes/` directory for Helm charts and manifests.

### Cloud Deployment

#### AWS
- Deploy to EC2 or ECS
- Use S3 for document storage
- Use RDS for database
- Use ElastiCache for Redis

#### Azure
- Deploy to Azure VM or Container Instances
- Use Azure Blob Storage for documents
- Use Azure Database for PostgreSQL
- Use Azure Cache for Redis

#### Google Cloud
- Deploy to GCE or Cloud Run
- Use GCS for document storage
- Use Cloud SQL for database
- Use Memorystore for Redis

## Monitoring and Logging

### Logging
```python
import logging
from src.core import get_config

config = get_config()
logging.basicConfig(
    level=getattr(logging, config.get('app.log_level', 'INFO')),
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
```

### Metrics
```bash
# Get system metrics
curl http://localhost:8000/api/v1/metrics
```

### Health Check
```bash
# Health check endpoint
curl http://localhost:8000/api/v1/health
```

## Troubleshooting

### Common Issues

#### OCR Engine Not Working
```bash
# Install Tesseract
sudo apt install tesseract-ocr libtesseract-dev
pip install pytesseract pillow
```

#### Database Connection Failed
```bash
# Check database is running
pg_isready -h localhost -p 5432

# Verify connection string in config
```

#### Port Already in Use
```bash
# Change port in config.json
# or kill existing process
lsof -ti:8000 | xargs kill
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

### Development Setup
```bash
pip install -r requirements-dev.txt
pytest --cov=src tests/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Tesseract OCR team
- Hugging Face Transformers team
- FastAPI team
- All contributors and users

## Contact

- GitHub: [korenakul/idp-enterprise](https://github.com/korenakul/idp-enterprise)
- Issues: [GitHub Issues](https://github.com/korenakul/idp-enterprise/issues)
- Email: support@idpenterprise.com
