"""
Document Service for IDP Enterprise Document Intelligence Platform.
Handles document processing, extraction, and workflow orchestration.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger('idp.services.document_service')


class DocumentService:
    """Service for managing document processing workflows."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.input_dir = Path(config.get('paths.input_dir', 'data/input'))
        self.output_dir = Path(config.get('paths.output_dir', 'data/output'))
        self.processed_dir = Path(config.get('paths.processed_dir', 'data/processed'))
        
        # Create directories
        for directory in [self.input_dir, self.output_dir, self.processed_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    def process_document(self, document_path: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """Process a single document."""
        path = Path(document_path)
        
        if not path.exists():
            return {'error': f'Document not found: {document_path}'}
        
        # Generate document ID
        doc_id = f"doc_{path.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        result = {
            'document_id': doc_id,
            'original_path': str(document_path),
            'filename': path.name,
            'file_type': path.suffix.lower(),
            'size_bytes': path.stat().st_size,
            'processed_at': datetime.now().isoformat(),
            'status': 'processing',
            'metadata': {},
            'extracted_data': {},
            'errors': []
        }
        
        # Validate document type
        result['metadata']['document_type'] = document_type or self._classify_document(path)
        
        # Mark as complete
        result['status'] = 'completed'
        
        # Save result
        self._save_result(result)
        
        logger.info(f"Processed document {doc_id}")
        return result
    
    def batch_process(self, documents: List[str], document_type: Optional[str] = None) -> Dict[str, Any]:
        """Process multiple documents in batch."""
        results = {
            'batch_id': f"batch_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'processed_at': datetime.now().isoformat(),
            'total_documents': len(documents),
            'successful': [],
            'failed': []
        }
        
        for doc_path in documents:
            try:
                result = self.process_document(doc_path, document_type)
                if result.get('status') == 'completed':
                    results['successful'].append(result)
                else:
                    results['failed'].append({
                        'path': doc_path,
                        'error': result.get('error', 'Unknown error')
                    })
            except Exception as e:
                results['failed'].append({
                    'path': doc_path,
                    'error': str(e)
                })
        
        results['summary'] = {
            'success_count': len(results['successful']),
            'failed_count': len(results['failed'])
        }
        
        return results
    
    def _classify_document(self, path: Path) -> str:
        """Classify document type based on content and filename patterns."""
        filename = path.name.lower()
        
        # Basic classification based on filename patterns
        if 'invoice' in filename:
            return 'invoice'
        elif 'contract' in filename or 'agreement' in filename:
            return 'contract'
        elif 'resume' in filename or 'cv' in filename:
            return 'resume'
        elif 'receipt' in filename:
            return 'receipt'
        elif 'statement' in filename:
            return 'bank_statement'
        elif 'passport' in filename:
            return 'passport'
        elif 'driver' in filename or 'license' in filename:
            return 'driver_license'
        elif 'medical' in filename:
            return 'medical_record'
        elif 'form' in filename:
            return 'form'
        else:
            return 'general_document'
    
    def _save_result(self, result: Dict[str, Any]) -> str:
        """Save processing result to output directory."""
        output_path = self.output_dir / f"{result['document_id']}.json"
        
        import json
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2, default=str)
        
        return str(output_path)
    
    def get_document(self, doc_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a processed document."""
        output_file = self.output_dir / f"{doc_id}.json"
        
        if output_file.exists():
            import json
            with open(output_file, 'r') as f:
                return json.load(f)
        return None
    
    def search_documents(self, query: str, document_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search processed documents."""
        results = []
        
        for json_file in self.output_dir.glob('*.json'):
            try:
                import json
                with open(json_file, 'r') as f:
                    doc = json.load(f)
                
                # Match query
                doc_str = str(doc).lower()
                if query.lower() in doc_str:
                    if document_type is None or doc.get('metadata', {}).get('document_type') == document_type:
                        results.append(doc)
            except Exception:
                continue
        
        return results
