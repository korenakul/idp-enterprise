"""Unit tests for core module."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from src.core import get_config


def test_get_config():
    """Test configuration loading."""
    config = get_config()
    assert config is not None
    assert config.get('app.name') == 'TrainPlex DIP'
    assert config.get('app.version') == '2.0.0'


def test_config_defaults():
    """Test default configuration values."""
    config = get_config()
    assert 'ocr' in config.config
    assert 'api' in config.config
    assert 'database' in config.config


if __name__ == '__main__':
    test_get_config()
    test_config_defaults()
    print("All core tests passed!")
