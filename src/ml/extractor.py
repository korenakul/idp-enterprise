"""
Information Extractor for IDP Enterprise Document Intelligence Platform.
Template-based and ML-based information extraction.
"""

import re
from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger('idp.ml.extractor')


class InformationExtractor:
    """Extract information from documents."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.extraction_rules = self._load_extraction_rules()
    
    def _load_extraction_rules(self) -> Dict[str, Dict[str, Any]]:
        """Load extraction rules for common document types."""
        return {
            'invoice': {
                'invoice_number': r'(?:invoice|invoice\s*#|inv(?:oice)?\s*no\.?)\s*[:\-]?\s*([A-Z0-9\-]+)',
                'date': r'(?:date|inv(?:oice)?\s*date)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                'amount': r'(?:total|amount\s*due|balance)\s*[:\-]?\s*\$?(\d+\.?\d*)',
                'vendor': r'(?:from|vendor|seller)\s*[:\-]?\s*([A-Z][a-zA-Z\s]+?)(?:\n|$)',
                'customer': r'(?:to|customer|bill\s*to)\s*[:\-]?\s*([A-Z][a-zA-Z\s]+?)(?:\n|$)'
            },
            'contract': {
                'parties': r'(?:party|between)\s*[:\-]?\s*([A-Z][a-zA-Z\s,]+?)(?:\n|$)',
                'effective_date': r'(?:effective|dated)\s*[:\-]?\s*(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                'term': r'(?:term|period|duration)\s*[:\-]?\s*(\d+\s*(?:day|month|year))',
                'amount': r'(?:amount|value|consideration)\s*[:\-]?\s*\$?(\d+\.?\d*)'
            },
            'resume': {
                'name': r'^([A-Z][A-Z\s]+)\n',
                'email': r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
                'phone': r'(\+?1?\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4})',
                'address': r'(\d+\s+[A-Za-z]+\s+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|[A-Z]{2})\s*\d*)',
                'linkedin': r'(?:linkedin\.com/in/)([a-zA-Z0-9_-]+)'
            },
            'passport': {
                'name': r'(?:Surname|Family Name)[:\s]+([A-Z\s]+?)(?:\n|$)',
                'given_name': r'(?:Given Names?|First Name)[:\s]+([A-Z\s]+?)(?:\n|$)',
                'passport_number': r'(?:Passport No\.?|Passport Number)[:\s]+([A-Z0-9]+)',
                'date_of_birth': r'(?:Date of Birth|Birth)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                'place_of_birth': r'(?:Place of Birth)[:\s]+([A-Z][a-zA-Z\s,]+?)(?:\n|$)',
                'expiration': r'(?:Date of Expiry|Exp)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            },
            'driver_license': {
                'name': r'(?:Name)[:\s]+([A-Z][a-zA-Z\s]+?)(?:\n|$)',
                'license_number': r'(?:License No\.?|DL No\.?)[:\s]+([A-Z0-9]+)',
                'address': r'(?:Address)[:\s]+(\d+\s+[A-Za-z\s]+)',
                'dob': r'(?:Date of Birth|DOB)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                'expiry': r'(?:Exp Date|Expires)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            },
            'medical_record': {
                'patient_name': r'(?:Patient Name|Name)[:\s]+([A-Z][a-zA-Z\s]+?)(?:\n|$)',
                'patient_id': r'(?:Medical Record No\.?|MRN|Patient ID)[:\s]+([A-Z0-9]+)',
                'date_of_birth': r'(?:Date of Birth|DOB)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})',
                'diagnosis': r'(?:Diagnosis|Conditions)[:\s]+([A-Z][a-zA-Z\s,]+?)(?:\n|$)',
                'date': r'(?:Date|Visit Date)[:\s]+(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
            }
        }
    
    def extract(self, text: str, document_type: Optional[str] = None) -> Dict[str, Any]:
        """Extract information from text based on document type."""
        results = {}
        
        # Determine document type if not provided
        doc_type = document_type or self._detect_document_type(text)
        
        # Extract using rules for the document type
        if doc_type in self.extraction_rules:
            for field, pattern in self.extraction_rules[doc_type].items():
                matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
                if matches:
                    results[field] = matches[0].strip() if isinstance(matches[0], str) else matches[0]
        
        # Extract generic patterns
        results.update(self._extract_generic(text))
        
        return {
            'document_type': doc_type,
            'extracted_data': results,
            'fields_found': len(results)
        }
    
    def _extract_generic(self, text: str) -> Dict[str, Any]:
        """Extract generic patterns from text."""
        results = {}
        
        # Extract dates
        date_pattern = r'(\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4})'
        dates = re.findall(date_pattern, text)
        if dates:
            results['dates'] = dates[:10]
        
        # Extract monetary amounts
        money_pattern = r'\$?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
        amounts = re.findall(money_pattern, text)
        if amounts:
            results['monetary_amounts'] = list(set(amounts))[:10]
        
        # Extract emails
        email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
        emails = re.findall(email_pattern, text)
        if emails:
            results['emails'] = emails[:5]
        
        # Extract phone numbers
        phone_pattern = r'(\+?1?\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4})'
        phones = re.findall(phone_pattern, text)
        if phones:
            results['phones'] = phones[:5]
        
        # Extract URLs
        url_pattern = r'(https?://[^\s]+|www\.[^\s]+)'
        urls = re.findall(url_pattern, text)
        if urls:
            results['urls'] = urls[:5]
        
        return results
    
    def _detect_document_type(self, text: str) -> str:
        """Automatically detect document type from content."""
        text_lower = text.lower()
        
        type_scores = {
            'invoice': sum(1 for kw in ['invoice', 'total due', 'amount due', 'invoice #'] if kw in text_lower),
            'contract': sum(1 for kw in ['contract', 'agreement', 'party of', 'terms and conditions'] if kw in text_lower),
            'resume': sum(1 for kw in ['resume', 'curriculum vitae', 'education', 'experience'] if kw in text_lower),
            'receipt': sum(1 for kw in ['receipt', 'thank you', 'total', 'cashier'] if kw in text_lower),
            'bank_statement': sum(1 for kw in ['bank statement', 'account number', 'transactions', 'balance'] if kw in text_lower),
            'passport': sum(1 for kw in ['passport', 'nationality', 'date of birth', 'place of birth'] if kw in text_lower),
            'driver_license': sum(1 for kw in ['driver license', 'license', 'class', 'endorsements'] if kw in text_lower),
            'medical_record': sum(1 for kw in ['medical record', 'patient', 'diagnosis', 'prescription'] if kw in text_lower),
            'form': sum(1 for kw in ['form', 'submit', 'signature', 'date'] if kw in text_lower)
        }
        
        if not type_scores:
            return 'general_document'
        
        return max(type_scores, key=type_scores.get) if any(type_scores.values()) else 'general_document'


def get_extractor(config: Dict[str, Any]) -> InformationExtractor:
    """Get information extractor instance."""
    return InformationExtractor(config)
