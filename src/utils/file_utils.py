"""
File utilities for IDP Enterprise Document Intelligence Platform.
"""

import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import logging

logger = logging.getLogger('idp.utils.file_utils')


def get_file_info(path: str) -> dict:
    """Get file information."""
    p = Path(path)
    if not p.exists():
        return {'error': 'File not found'}
    
    stat = p.stat()
    return {
        'name': p.name,
        'size_bytes': stat.st_size,
        'size_mb': round(stat.st_size / (1024 * 1024), 2),
        'extension': p.suffix.lower(),
        'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
        'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        'is_file': p.is_file(),
        'is_directory': p.is_dir()
    }


def find_documents(directory: str, extensions: Optional[List[str]] = None) -> List[Path]:
    """Find documents in directory."""
    if extensions is None:
        extensions = ['.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.docx', '.txt']
    
    dir_path = Path(directory)
    if not dir_path.exists():
        return []
    
    documents = []
    for ext in extensions:
        documents.extend(dir_path.glob(f'*{ext}'))
        documents.extend(dir_path.glob(f'**/*{ext}'))
    
    return list(set(documents))


def ensure_directory(path: str) -> Path:
    """Ensure directory exists, create if not."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def get_file_hash(path: str) -> str:
    """Get SHA256 hash of file."""
    import hashlib
    
    sha256 = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            sha256.update(chunk)
    return sha256.hexdigest()


def safe_delete(path: str) -> bool:
    """Safely delete file."""
    try:
        p = Path(path)
        if p.exists():
            p.unlink()
            return True
        return False
    except Exception as e:
        logger.error(f"Failed to delete {path}: {e}")
        return False
