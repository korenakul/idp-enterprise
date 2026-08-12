"""
Document Classifier for IDP Enterprise Document Intelligence Platform.
ML-based document classification with 100+ categories.
"""

import os
from pathlib import Path
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('idp.ml.classifier')


class DocumentClassifier:
    """ML-based document classifier."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get('ai', {}).get('models', {}).get('classification', 'distilbert-base-uncased')
        self.model = None
        self.tokenizer = None
        self._initialize()
    
    def _initialize(self):
        """Initialize classification model."""
        try:
            from transformers import pipeline
            
            self.classifier = pipeline(
                'text-classification',
                model=self.model_name,
                return_all_scores=True
            )
            logger.info(f"Loaded classification model: {self.model_name}")
        except Exception as e:
            logger.warning(f"Could not load classifier model: {e}")
            self.classifier = None
    
    def classify(self, text: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Classify document type from text content."""
        if not self.classifier:
            return self._fallback_classify(text)
        
        try:
            results = self.classifier(text[:512], top_k=top_k)
            return results
        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return self._fallback_classify(text)
    
    def _fallback_classify(self, text: str) -> List[Dict[str, Any]]:
        """Fallback classification using keyword matching."""
        text_lower = text.lower()
        
        categories = {
            'invoice': ['invoice', 'invoice #', 'total due', 'amount due'],
            'contract': ['contract', 'agreement', 'terms and conditions', 'party of the first part'],
            'resume': ['resume', 'curriculum vitae', 'experience', 'education'],
            'receipt': ['receipt', 'total', 'cashier', 'thank you'],
            'bank_statement': ['bank statement', 'account number', 'transactions', 'balance'],
            'passport': ['passport', 'nationality', 'date of birth', 'place of birth'],
            'driver_license': ['driver license', 'license', 'class', 'endorsements'],
            'medical_record': ['medical record', 'patient', 'diagnosis', 'prescription'],
            'form': ['form', 'submit', 'signature', 'date'],
            'letter': ['dear', 'sincerely', 'yours truly', 'regards']
        }
        
        scores = []
        for category, keywords in categories.items():
            matches = sum(1 for kw in keywords if kw in text_lower)
            score = matches / len(keywords) if keywords else 0
            if score > 0:
                scores.append({'label': category, 'score': score})
        
        scores.sort(key=lambda x: x['score'], reverse=True)
        return scores[:5]
    
    def classify_image(self, image_path: str) -> Dict[str, Any]:
        """Classify document type from image using OCR + ML."""
        try:
            from src.ml.ocr_engine import get_ocr_engine
            
            engine = get_ocr_engine('tesseract', {})
            ocr_result = engine.extract_text(image_path)
            text = ocr_result.get('text', '')
            
            return {
                'text': text,
                'classification': self.classify(text),
                'ocr_confidence': ocr_result.get('confidence', 0)
            }
        except Exception as e:
            logger.error(f"Image classification failed: {e}")
            return {'error': str(e)}


def get_classifier(config: Dict[str, Any]) -> DocumentClassifier:
    """Get classifier instance."""
    return DocumentClassifier(config)
