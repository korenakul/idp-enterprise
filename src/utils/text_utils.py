"""
Text utilities for TrainPlex Document Intelligence Platform.
"""

import re
from typing import List, Optional, Dict, Any
from collections import Counter
import logging

logger = logging.getLogger('trainplex.utils.text_utils')


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ''
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text)
    # Remove special characters (preserve basic punctuation)
    text = re.sub(r'[^\w\s.,!?;:\'"()\-\n]', '', text)
    return text.strip()


def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text."""
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return list(set(re.findall(pattern, text)))


def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text."""
    patterns = [
        r'\+?1?\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}',
        r'\d{3}[\s\-]\d{3}[\s\-]\d{4}'
    ]
    phones = []
    for pattern in patterns:
        phones.extend(re.findall(pattern, text))
    return list(set(phones))


def extract_dates(text: str) -> List[str]:
    """Extract dates from text."""
    patterns = [
        r'\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}',
        r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}'
    ]
    dates = []
    for pattern in patterns:
        dates.extend(re.findall(pattern, text))
    return list(set(dates))


def extract_monetary_values(text: str) -> List[str]:
    """Extract monetary values from text."""
    pattern = r'\$?\s*(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    return re.findall(pattern, text)


def extract_urls(text: str) -> List[str]:
    """Extract URLs from text."""
    pattern = r'https?://[^\s]+|www\.[^\s]+'
    return list(set(re.findall(pattern, text)))


def extract_names(text: str) -> List[str]:
    """Extract potential names from text."""
    # Simple heuristic for capitalized words
    pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
    return list(set(re.findall(pattern, text)))


def count_words(text: str) -> Dict[str, int]:
    """Count word frequencies."""
    words = re.findall(r'\b\w+\b', text.lower())
    return dict(Counter(words).most_common(20))


def extract_field_value(text: str, field_name: str) -> Optional[str]:
    """Extract value for a specific field name."""
    patterns = [
        rf'{field_name}\s*[:\-]?\s*([^\n]+)',
        rf'{field_name}\s*[:\-]?\s*\w+\s*[:\-]?\s*([^\n]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Validate phone format."""
    pattern = r'^\+?1?\s*\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{4}$'
    return bool(re.match(pattern, phone))
