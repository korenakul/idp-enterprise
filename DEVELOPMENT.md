# TrainPlex Document Intelligence Platform - Development Guide

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Tesseract OCR (optional, for local OCR)

### Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/your-username/trainplex-dip.git
cd trainplex-dip
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate    # Windows
```

3. **Install development dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. **Configure for development**
```bash
cp config.example.json config.json
# Edit config.json for local development
```

5. **Set up database**
```bash
createdb trainplex_dip_dev
# Run migrations if using Alembic
alembic upgrade head
```

## Project Structure

```
src/
├── __init__.py              # Package initialization
├── main.py                  # Application entry point
├── config.py                # Configuration management
│
├── core/                    # Core utilities
│   ├── __init__.py
│   └── config.py            # Configuration management
│
├── ml/                      # Machine learning & OCR
│   ├── __init__.py
│   ├── ocr_engine.py        # OCR engine implementations
│   ├── classifier.py        # Document classification
│   ├── extractor.py         # Information extraction
│   └── extraction.py        # Extraction models
│
├── services/                # Business logic
│   ├── __init__.py
│   └── document_service.py  # Document processing service
│
├── workers/                 # Background processing
│   ├── __init__.py
│   ├── processor.py         # Document processor
│   └── queue_processor.py   # Queue-based processing
│
├── database/                # Database layer
│   ├── __init__.py
│   ├── models.py            # SQLAlchemy models
│   └── manager.py           # Database manager
│
├── api/                     # REST API
│   ├── __init__.py
│   ├── server.py            # FastAPI application
│   └── routes.py            # API routes
│
├── cli/                     # Command-line interface
│   ├── __init__.py
│   └── cli.py               # CLI implementation
│
├── integrations/            # External system integrations
│   ├── __init__.py
│   ├── erp.py               # ERP connectors
│   └── crm.py               # CRM connectors
│
├── utils/                   # Utility functions
│   ├── __init__.py
│   ├── file_utils.py        # File operations
│   ├── text_utils.py        # Text processing
│   └── image_utils.py       # Image operations
│
└── models/                  # Pydantic models
    └── __init__.py
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guidelines
- Use 4 spaces for indentation
- Max line length: 88 characters (Black formatter)
- Use type hints for all functions
- Write docstrings for all public modules/classes/functions

### Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Modules | lowercase_with_underscore | `ocr_engine.py` |
| Classes | CapitalizedWords | `DocumentService` |
| Functions | lowercase_with_underscore | `get_config()` |
| Variables | lowercase_with_underscore | `document_id` |
| Constants | UPPERCASE_WITH_UNDERSCORE | `MAX_RETRIES` |

### Type Hints

```python
from typing import Dict, Any, Optional, List

def process_document(
    document_path: str,
    document_type: Optional[str] = None
) -> Dict[str, Any]:
    """Process a document."""
    result: Dict[str, Any] = {
        'status': 'pending',
        'document_id': ''
    }
    return result
```

### Logging

```python
import logging

logger = logging.getLogger('trainplex.module.name')

def process_document(path: str):
    logger.debug(f"Processing: {path}")
    logger.info(f"Started processing: {path}")
    logger.warning(f"Document may be corrupted: {path}")
    logger.error(f"Failed to process: {path}", exc_info=True)
```

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Tests
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# Specific test file
pytest tests/test_core.py -v
```

### Run with Coverage
```bash
pytest --cov=src --cov-report=html tests/
# View coverage report
open htmlcov/index.html
```

### Run Tests in Parallel
```bash
pytest -n auto tests/
```

## Debugging

### Enable Debug Logging
```bash
# In config.json
{
  "app": {
    "log_level": "DEBUG"
  }
}

# Or via environment
export LOG_LEVEL=DEBUG
```

### Debug with pdb
```python
import pdb

def process_document(path: str):
    pdb.set_trace()
    # ... rest of code
```

### Debug API Requests
```bash
# Add verbose logging to curl
curl -v -X POST http://localhost:8000/api/v1/documents/extract \
  -F "file=@document.pdf"
```

## Common Development Tasks

### Adding a New OCR Engine

1. **Create engine class**
```python
# src/ml/ocr_engine.py

class NewEngine(BaseOCREngine):
    """New OCR engine implementation."""
    
    def extract_text(self, image_path: str, language: str = 'eng') -> Dict[str, Any]:
        # Implementation
        return {'text': '', 'confidence': 0}
```

2. **Register engine**
```python
def get_ocr_engine(engine_name: str, config: Dict[str, Any]) -> BaseOCREngine:
    engines = {
        'tesseract': TesseractEngine,
        'gemini': GeminiEngine,
        'new_engine': NewEngine,  # Add here
    }
    # ...
```

### Adding a New API Endpoint

1. **Define route**
```python
# src/api/routes.py

@router.post("/documents/analyze")
async def analyze_document(file: UploadFile = File(...)):
    """Analyze document."""
    return {"filename": file.filename, "status": "analyzing"}
```

2. **Register in main app**
```python
# src/api/server.py
app.include_router(router)
```

### Adding a New Document Type

1. **Update classification**
```python
# src/services/document_service.py

def _classify_document(self, path: Path) -> str:
    filename = path.name.lower()
    
    if 'new_document' in filename:
        return 'new_document'
    # ...
```

2. **Update extraction rules**
```python
# src/ml/extractor.py

def _load_extraction_rules(self) -> Dict[str, Dict[str, Any]]:
    return {
        'new_document': {
            'field1': r'pattern',
            'field2': r'pattern',
        },
        # ...
    }
```

## Performance Optimization

### Profiling
```bash
# Profile with cProfile
python -m cProfile -o profile.out main.py

# Visualize with SnakeViz
pip install snakeviz
snakeviz profile.out
```

### Optimization Tips

1. **Batch Processing**
```python
# Process multiple documents
results = processor.process_batch(documents)
```

2. **Lazy Loading**
```python
# Load models only when needed
def __init__(self):
    self._model = None

def _get_model(self):
    if self._model is None:
        self._model = load_model()
    return self._model
```

3. **Connection Pooling**
```python
# Database connection pooling
engine = create_engine(url, pool_size=10, max_overflow=20)
```

## CI/CD Pipeline

### GitHub Actions

```yaml
name: CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      - name: Run tests
        run: |
          pytest tests/ -v --cov=src
      - name: Upload coverage
        uses: actions/upload-artifact@v3
        with:
          name: coverage
          path: htmlcov/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest tests/ -v`)
5. Add documentation for new features
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Documentation

### Generate API Docs
```bash
# FastAPI auto-generates docs
# Visit http://localhost:8000/docs
```

### Generate Docstring Coverage
```bash
pip install pydocstyle
pydocstyle src/
```

## Troubleshooting

### Common Issues

**Issue**: OCR engine not working
```
Solution: Install Tesseract
sudo apt install tesseract-ocr libtesseract-dev
pip install pytesseract pillow
```

**Issue**: Database connection failed
```
Solution: Check PostgreSQL is running
pg_isready -h localhost -p 5432
```

**Issue**: Port already in use
```
Solution: Change port or kill process
lsof -ti:8000 | xargs kill
```

### Getting Help

- GitHub Issues: https://github.com/your-username/trainplex-dip/issues
- Documentation: https://trainplex-dip.readthedocs.io
- Email: dev@trainplex.com
