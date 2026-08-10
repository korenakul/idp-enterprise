"""
Document Processor Worker for TrainPlex Document Intelligence Platform.
Handles background document processing with OCR and AI extraction.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import json

logger = logging.getLogger('trainplex.workers.processor')


class DocumentProcessor:
    """Background document processor worker."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.ocr_engines = config.get('ocr', {}).get('engines', ['tesseract'])
        self.current_engine_index = 0
        self.metrics = {
            'total_processed': 0,
            'successful': 0,
            'failed': 0,
            'total_time_seconds': 0
        }
    
    def process(self, document_path: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """Process a document with all configured OCR engines."""
        import time
        
        start_time = time.time()
        path = Path(document_path)
        
        result = {
            'document_id': f"doc_{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'original_path': str(document_path),
            'filename': path.name,
            'processed_at': datetime.now().isoformat(),
            'status': 'pending',
            'ocr_results': [],
            'extracted_data': {},
            'metadata': {
                'file_type': path.suffix.lower(),
                'file_size': path.stat().st_size,
                'document_type': document_type or self._classify_document(path)
            }
        }
        
        try:
            result['status'] = 'processing'
            
            # Process with all OCR engines
            for engine_name in self.ocr_engines:
                engine_result = self._process_with_engine(document_path, engine_name)
                result['ocr_results'].append(engine_result)
                
                if engine_result.get('success'):
                    result['extracted_data'] = engine_result.get('data', {})
                    break
            
            result['status'] = 'completed'
            self.metrics['successful'] += 1
            
        except Exception as e:
            result['status'] = 'failed'
            result['error'] = str(e)
            self.metrics['failed'] += 1
            logger.error(f"Processing failed: {e}")
        
        elapsed = time.time() - start_time
        self.metrics['total_time_seconds'] += elapsed
        self.metrics['total_processed'] += 1
        
        return result
    
    def _process_with_engine(self, document_path: str, engine_name: str) -> Dict[str, Any]:
        """Process document with a specific OCR engine."""
        try:
            from src.ml.ocr_engine import get_ocr_engine
            
            engine_config = {
                'api_key': self.config.get(f'api_keys.{engine_name}'),
                'region': self.config.get(f'aws.region', 'us-east-1'),
                's3_bucket': self.config.get('aws.textract_s3_bucket', 'trainplex-documents')
            }
            
            engine = get_ocr_engine(engine_name, engine_config)
            result = engine.extract_text(document_path)
            
            return {
                'engine': engine_name,
                'success': result.get('text', '').strip() != '',
                'text': result.get('text', ''),
                'confidence': result.get('confidence', 0),
                'error': result.get('error')
            }
            
        except Exception as e:
            logger.error(f"Engine {engine_name} failed: {e}")
            return {
                'engine': engine_name,
                'success': False,
                'error': str(e)
            }
    
    def _classify_document(self, path: Path) -> str:
        """Classify document type based on filename patterns."""
        filename = path.name.lower()
        
        classifications = {
            'invoice': ['invoice'],
            'contract': ['contract', 'agreement'],
            'resume': ['resume', 'cv'],
            'receipt': ['receipt'],
            'bank_statement': ['statement', 'bank'],
            'passport': ['passport'],
            'driver_license': ['driver', 'license'],
            'medical_record': ['medical', 'health'],
            'form': ['form']
        }
        
        for doc_type, keywords in classifications.items():
            if any(kw in filename for kw in keywords):
                return doc_type
        
        return 'general_document'
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get processing metrics."""
        return {
            **self.metrics,
            'average_time': self.metrics['total_time_seconds'] / max(self.metrics['total_processed'], 1),
            'success_rate': self.metrics['successful'] / max(self.metrics['total_processed'], 1)
        }
    
    def process_batch(self, documents: List[str], document_type: Optional[str] = None) -> Dict[str, Any]:
        """Process multiple documents."""
        results = {
            'batch_id': f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'processed_at': datetime.now().isoformat(),
            'total': len(documents),
            'results': [],
            'metrics': {}
        }
        
        for doc_path in documents:
            try:
                result = self.process(doc_path, document_type)
                results['results'].append(result)
            except Exception as e:
                results['results'].append({
                    'document': doc_path,
                    'status': 'failed',
                    'error': str(e)
                })
        
        results['metrics'] = self.get_metrics()
        return results
