"""
OCR Engine implementations for IDP Enterprise Document Intelligence Platform.
"""

import os
import base64
from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger('idp.ml.ocr_engine')


class BaseOCREngine:
    """Base OCR engine interface."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
    
    def extract_text(self, image_path: str, language: str = 'eng') -> Dict[str, Any]:
        raise NotImplementedError


class TesseractEngine(BaseOCREngine):
    """Tesseract OCR engine implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self._initialize()
    
    def _initialize(self):
        """Initialize Tesseract engine."""
        try:
            import pytesseract
            self.engine = pytesseract
        except ImportError:
            logger.warning("pytesseract not installed. Install with: pip install pytesseract pillow")
            self.engine = None
    
    def extract_text(self, image_path: str, language: str = 'eng') -> Dict[str, Any]:
        if not self.engine:
            return {'text': '', 'confidence': 0, 'error': 'Tesseract not available'}
        
        try:
            from PIL import Image
            image = Image.open(image_path)
            data = self.engine.image_to_data(image, lang=language, output_type=self.engine.Output.DICT)
            
            text = ' '.join(data['text'])
            confidence = sum(d for d in data['conf'] if d > 0) / max(len([d for d in data['conf'] if d > 0]), 1)
            
            return {
                'text': text,
                'confidence': confidence / 100,
                'words': [{'text': w, 'confidence': c/100, 'bbox': [x, y, w, h]} 
                         for w, c, x, y, w, h in zip(data['text'], data['conf'], data['left'], data['top'], data['width'], data['height'])],
                'language': language
            }
        except Exception as e:
            logger.error(f"Tesseract extraction failed: {e}")
            return {'text': '', 'confidence': 0, 'error': str(e)}


class GeminiEngine(BaseOCREngine):
    """Google Gemini OCR engine implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.api_key = config.get('api_key')
        self.model = config.get('model', 'gemini-1.5-flash')
    
    def extract_text(self, image_path: str, language: str = 'eng') -> Dict[str, Any]:
        if not self.api_key:
            return {'text': '', 'confidence': 0, 'error': 'Gemini API key not configured'}
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            
            image_file = Path(image_path)
            with open(image_file, 'rb') as f:
                image_data = f.read()
            
            model = genai.GenerativeModel(self.model)
            prompt = f"Extract all text from this document image in {language}. Output as JSON with text and confidence score."
            response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': base64.b64encode(image_data).decode()}])
            
            return {
                'text': response.text,
                'confidence': 0.9,
                'model': self.model,
                'language': language
            }
        except Exception as e:
            logger.error(f"Gemini extraction failed: {e}")
            return {'text': '', 'confidence': 0, 'error': str(e)}


class AWSlextractEngine(BaseOCREngine):
    """AWS Textract OCR engine implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.region = config.get('region', 'us-east-1')
    
    def extract_text(self, image_path: str, language: str = 'eng') -> Dict[str, Any]:
        try:
            import boto3
            s3 = boto3.client('s3', region_name=self.region)
            textract = boto3.client('textract', region_name=self.region)
            
            # Upload to S3 first
            bucket = self.config.get('s3_bucket', 'idp-documents')
            key = f'textract/{Path(image_path).name}'
            s3.upload_file(image_path, bucket, key)
            
            # Call Textract
            response = textract.analyze_document(
                Document={'S3Object': {'Bucket': bucket, 'Name': key}},
                Features=['FORMS', 'TABLES']
            )
            
            text = self._extract_text_from_textract(response)
            return {'text': text, 'confidence': 0.95, 'raw': response}
        except Exception as e:
            logger.error(f"AWS Textract failed: {e}")
            return {'text': '', 'confidence': 0, 'error': str(e)}
    
    def _extract_text_from_textract(self, response: Dict) -> str:
        """Extract text from Textract response."""
        text = []
        for block in response.get('Blocks', []):
            if block.get('BlockType') == 'WORD':
                text.append(block.get('Text', ''))
        return ' '.join(text)


def get_ocr_engine(engine_name: str, config: Dict[str, Any]) -> BaseOCREngine:
    """Factory function to get OCR engine."""
    engines = {
        'tesseract': TesseractEngine,
        'gemini': GeminiEngine,
        'aws_textract': AWSlextractEngine
    }
    
    if engine_name not in engines:
        logger.warning(f"Unknown engine {engine_name}, using tesseract")
        engine_name = 'tesseract'
    
    return engines[engine_name](config)
