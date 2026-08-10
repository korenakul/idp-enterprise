"""
Configuration management for TrainPlex Document Intelligence Platform.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger('trainplex.core.config')


def safe_json_load(path: str, default: Any = None) -> Any:
    """Safely load JSON file with fallback."""
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logger.warning(f"Could not load JSON from {path}")
        return default


def safe_json_save(data: Any, path: str) -> bool:
    """Safely save data to JSON file."""
    try:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            json.dump(data, f, indent=2, default=str)
        return True
    except Exception as e:
        logger.error(f"Could not save JSON to {path}: {e}")
        return False


class ConfigManager:
    """Centralized configuration management."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self._validate_config()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        defaults = {
            'app': {'name': 'TrainPlex DIP', 'version': '2.0.0', 'log_level': 'INFO', 'debug': False, 'timezone': 'UTC'},
            'paths': {'input_dir': 'data/input', 'output_dir': 'data/output', 'processed_dir': 'data/processed', 'cache_dir': 'data/cache', 'models_dir': 'data/models', 'logs_dir': 'logs'},
            'ocr': {'engines': ['tesseract', 'gemini', 'aws_textract', 'azure_ocr', 'google_vision'], 'default_engine': 'tesseract', 'languages': ['eng', 'hin', 'spa', 'fra'], 'confidence_threshold': 0.8},
            'ai': {'models': {'classification': 'distilbert-base-uncased', 'extraction': 'gemini-1.5-flash', 'ner': 'en_core_web_sm'}, 'batch_size': 32, 'max_sequence_length': 512},
            'api': {'host': '0.0.0.0', 'port': 8000, 'workers': 4, 'rate_limit': 100, 'timeout': 300},
            'database': {'type': 'postgresql', 'host': 'localhost', 'port': 5432, 'name': 'trainplex_dip', 'pool_size': 10},
            'queue': {'type': 'redis', 'host': 'localhost', 'port': 6379, 'queue_name': 'dip_tasks'},
            'aws': {'region': 'us-east-1', 'textract_s3_bucket': 'trainplex-documents'},
            'integration': {'erp': {'enabled': False, 'type': 'sap'}, 'crm': {'enabled': False, 'type': 'salesforce'}},
            'monitoring': {'metrics': True, 'tracing': True, 'health_check_interval': 30}
        }
        if config_path and os.path.exists(config_path):
            user_config = safe_json_load(config_path, {})
            self._merge_config(defaults, user_config)
        return defaults
    
    def _merge_config(self, defaults: Dict, user_config: Dict) -> None:
        for key, value in user_config.items():
            if key in defaults and isinstance(defaults[key], dict) and isinstance(value, dict):
                self._merge_config(defaults[key], value)
            else:
                defaults[key] = value
    
    def _validate_config(self) -> None:
        for path_key in ['input_dir', 'output_dir', 'processed_dir']:
            path = self.get(f'paths.{path_key}')
            Path(path).mkdir(parents=True, exist_ok=True)
        logger.info(f"Configuration loaded for {self.get('app.name')}")
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def update(self, key: str, value: Any) -> None:
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config or not isinstance(config[k], dict):
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
    
    def save(self, path: str) -> None:
        safe_json_save(self.config, path)


_config_manager = None


def get_config() -> ConfigManager:
    global _config_manager
    if _config_manager is None:
        config_path = os.environ.get('DIP_CONFIG_PATH')
        _config_manager = ConfigManager(config_path)
    return _config_manager
