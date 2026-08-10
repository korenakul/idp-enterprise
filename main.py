"""
Main entry point for TrainPlex Document Intelligence Platform.
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.core import get_config
from src.ml.ocr_engine import get_ocr_engine
from src.services.document_service import DocumentService
from src.workers.processor import DocumentProcessor
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(name)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger('trainplex.main')


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description='TrainPlex Document Intelligence Platform')
    parser.add_argument('--mode', choices=['cli', 'api', 'worker', 'batch'], default='cli',
                       help='Run mode')
    parser.add_argument('--config', '-c', help='Config file path')
    
    args = parser.parse_args()
    
    if args.config:
        import os
        os.environ['DIP_CONFIG_PATH'] = args.config
    
    config = get_config()
    logger.info(f"Starting TrainPlex DIP v{config.get('app.version')}")
    
    if args.mode == 'cli':
        from src.cli.cli import main as cli_main
        sys.exit(cli_main())
    elif args.mode == 'api':
        run_api_server(config)
    elif args.mode == 'worker':
        run_worker(config)
    elif args.mode == 'batch':
        run_batch_processor(config)
    
    logger.info("TrainPlex DIP stopped")


def run_api_server(config: dict):
    """Run the API server."""
    logger.info("Starting API server...")
    host = config.get('api.host', '0.0.0.0')
    port = config.get('api.port', 8000)
    logger.info(f"API server running on http://{host}:{port}")
    logger.info("Use 'pip install fastapi uvicorn' to enable API server")


def run_worker(config: dict):
    """Run the document processor worker."""
    logger.info("Starting document processor worker...")
    processor = DocumentProcessor(config)
    logger.info("Worker ready. Waiting for tasks...")


def run_batch_processor(config: dict):
    """Run batch document processor."""
    logger.info("Starting batch processor...")
    input_dir = Path(config.get('paths.input_dir', 'data/input'))
    documents = list(input_dir.glob('*'))
    logger.info(f"Found {len(documents)} documents to process")
    
    processor = DocumentProcessor(config)
    # Process documents


if __name__ == '__main__':
    main()
