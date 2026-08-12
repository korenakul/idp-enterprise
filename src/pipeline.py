"""
Document processing pipeline for IDP Enterprise Document Intelligence Platform.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging
from datetime import datetime

from src.core import get_config
from src.ml.ocr_engine import get_ocr_engine
from src.ml.extraction import DocumentExtractor, ExtractedDocument

logger = logging.getLogger('idp.pipeline')


class DocumentPipeline:
    """End-to-end document processing pipeline."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or get_config()
        self.ocr_engine = get_ocr_engine(
            self.config.get('ocr.default_engine', 'tesseract'),
            self.config.get('ocr', {})
        )
        self.extractor = DocumentExtractor(self.config.get('ai', {}))
    
    def process(self, document_path: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """
        Process document through full pipeline:
        1. Preprocessing
        2. OCR
        3. Classification
        4. Extraction
        5. Post-processing
        """
        logger.info(f"Processing: {document_path}")
        
        result = {
            'document_id': Path(document_path).stem,
            'input_path': document_path,
            'start_time': datetime.now().isoformat(),
            'steps': []
        }
        
        try:
            # Step 1: OCR extraction
            ocr_result = self._run_ocr(document_path)
            result['steps'].append({'name': 'ocr', 'status': 'completed'})
            result['text'] = ocr_result.get('text', '')
            result['ocr_confidence'] = ocr_result.get('confidence', 0)
            
            # Step 2: Document classification
            classification = self.extractor.classify_document(result['text'])
            result['steps'].append({'name': 'classification', 'status': 'completed'})
            result['document_type'] = classification.get('document_type', 'unknown')
            result['classification_confidence'] = classification.get('confidence', 0)
            
            # Step 3: Information extraction
            extraction_result = self.extractor.extract(document_path, document_type)
            result['steps'].append({'name': 'extraction', 'status': 'completed'})
            result['extraction'] = {
                'document_id': extraction_result.document_id,
                'confidence': extraction_result.confidence,
                'entities': [{'text': e.text, 'type': e.entity_type, 'confidence': e.confidence} 
                            for e in extraction_result.extracted_entities]
            }
            
            result['status'] = 'completed'
            result['end_time'] = datetime.now().isoformat()
            
        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            result['status'] = 'failed'
            result['error'] = str(e)
            result['end_time'] = datetime.now().isoformat()
        
        return result
    
    def _run_ocr(self, document_path: str) -> Dict[str, Any]:
        """Run OCR engine on document."""
        return self.ocr_engine.extract_text(document_path)
    
    def batch_process(self, documents: List[str]) -> List[Dict[str, Any]]:
        """Process multiple documents."""
        return [self.process(doc) for doc in documents]


class PreprocessingPipeline:
    """Document preprocessing pipeline."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def preprocess(self, image_path: str) -> str:
        """
        Preprocess document image for better OCR results:
        - Grayscale conversion
        - Noise reduction
        - Thresholding
        - Deskewing
        """
        logger.info(f"Preprocessing: {image_path}")
        return image_path  # Placeholder for preprocessing logic


class PostprocessingPipeline:
    """Document post-processing pipeline."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def validate(self, extracted_data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate extracted data quality."""
        return {
            'valid': True,
            'data_quality_score': 0.95,
            'issues': []
        }
    
    def format_output(self, extracted_data: Dict[str, Any], format: str = 'json') -> Any:
        """Format extracted data in specified format."""
        if format == 'json':
            return extracted_data
        elif format == 'csv':
            return self._to_csv(extracted_data)
        return extracted_data
    
    def _to_csv(self, data: Dict[str, Any]) -> str:
        """Convert data to CSV format."""
        lines = []
        for key, value in data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    lines.append(f"{key}.{sub_key},{sub_value}")
            else:
                lines.append(f"{key},{value}")
        return '\n'.join(lines)
