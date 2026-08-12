"""
Image utilities for IDP Enterprise Document Intelligence Platform.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple
from datetime import datetime
import logging

logger = logging.getLogger('idp.utils.image_utils')


def get_image_info(path: str) -> dict:
    """Get image information."""
    from PIL import Image
    
    p = Path(path)
    if not p.exists():
        return {'error': 'File not found'}
    
    try:
        with Image.open(p) as img:
            return {
                'name': p.name,
                'format': img.format,
                'mode': img.mode,
                'size': {'width': img.size[0], 'height': img.size[1]},
                'dpi': img.info.get('dpi'),
                'created': datetime.fromtimestamp(p.stat().st_ctime).isoformat()
            }
    except Exception as e:
        return {'error': str(e)}


def convert_image_format(input_path: str, output_format: str = 'JPEG') -> Optional[str]:
    """Convert image to different format."""
    from PIL import Image
    
    p = Path(input_path)
    output_path = p.with_suffix(f'.{output_format.lower()}')
    
    try:
        with Image.open(p) as img:
            rgb_img = img.convert('RGB')
            rgb_img.save(output_path, output_format)
        return str(output_path)
    except Exception as e:
        logger.error(f"Conversion failed: {e}")
        return None


def crop_document(image_path: str, padding: int = 10) -> Optional[str]:
    """Crop document from image."""
    from PIL import Image
    
    try:
        with Image.open(image_path) as img:
            width, height = img.size
            # Simple crop with padding
            bbox = (padding, padding, width - padding, height - padding)
            cropped = img.crop(bbox)
            
            output_path = Path(image_path).with_name(f"cropped_{Path(image_path).name}")
            cropped.save(output_path)
            return str(output_path)
    except Exception as e:
        logger.error(f"Cropping failed: {e}")
        return None


def get_image_dpi(image_path: str) -> Optional[Tuple[int, int]]:
    """Get image DPI."""
    from PIL import Image
    
    try:
        with Image.open(image_path) as img:
            return img.info.get('dpi', (72, 72))
    except Exception:
        return None
