"""Unit tests for services module."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.services.document_service import DocumentService
from src.core import get_config


def test_document_service_init():
    """Test DocumentService initialization."""
    config = get_config()
    service = DocumentService(config.config)
    assert service is not None
    assert hasattr(service, 'input_dir')
    assert hasattr(service, 'output_dir')


def test_document_service_process():
    """Test document processing."""
    config = get_config()
    service = DocumentService(config.config)
    
    # Create a test file first
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test document content")
        test_file = f.name
    
    try:
        result = service.process_document(test_file, 'general_document')
        assert 'document_id' in result
        assert result.get('status') == 'completed'
    finally:
        import os
        os.unlink(test_file)


if __name__ == '__main__':
    test_document_service_init()
    test_document_service_process()
    print("All service tests passed!")
