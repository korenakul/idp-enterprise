"""
Command-line interface for IDP Enterprise Document Intelligence Platform.
"""

import sys
import argparse
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger('idp.cli')


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='IDP Enterprise Document Intelligence Platform CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --file document.pdf --type invoice
  %(prog)s --file document.pdf --extract --output results.json
  %(prog)s --batch input/*.pdf --type contract
  %(prog)s --search invoice --type invoice
        """
    )
    
    parser.add_argument('--file', '-f', help='Document file to process')
    parser.add_argument('--type', '-t', choices=['invoice', 'contract', 'resume', 'receipt', 
                                                 'bank_statement', 'passport', 'driver_license', 
                                                 'medical_record', 'form', 'general_document'],
                        help='Document type (auto-detected if not specified)')
    parser.add_argument('--extract', '-e', action='store_true', help='Extract information after processing')
    parser.add_argument('--output', '-o', help='Output file for results')
    parser.add_argument('--search', '-s', help='Search processed documents')
    parser.add_argument('--batch', '-b', help='Process batch of documents (glob pattern)')
    parser.add_argument('--config', '-c', help='Config file path')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
    
    if args.file:
        return process_single_file(args)
    elif args.batch:
        return process_batch(args)
    elif args.search:
        return search_documents(args)
    else:
        parser.print_help()
        return 0


def process_single_file(args) -> int:
    """Process a single document file."""
    from src.services.document_service import DocumentService
    from src.core import get_config
    
    config = get_config()
    service = DocumentService(config.config)
    
    if not Path(args.file).exists():
        logger.error(f"File not found: {args.file}")
        return 1
    
    logger.info(f"Processing: {args.file}")
    result = service.process_document(args.file, args.type)
    
    if result.get('status') == 'completed':
        logger.info(f"Document ID: {result['document_id']}")
        logger.info(f"Type: {result['metadata'].get('document_type', 'unknown')}")
        
        if args.extract:
            from src.ml.extractor import get_extractor
            from src.ml.ocr_engine import get_ocr_engine
            
            logger.info("\nExtracted Information:")
            extractor = get_extractor(config.config)
            ocr_engine = get_ocr_engine('tesseract', {})
            
            ocr_result = ocr_engine.extract_text(args.file)
            extraction = extractor.extract(ocr_result.get('text', ''), result['metadata'].get('document_type'))
            
            for field, value in extraction.get('extracted_data', {}).items():
                logger.info(f"  {field}: {value}")
        
        if args.output:
            import json
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            logger.info(f"Results saved to: {output_path}")
        
        return 0
    else:
        logger.error(f"Processing failed: {result.get('error', 'Unknown error')}")
        return 1


def process_batch(args) -> int:
    """Process a batch of documents."""
    from src.services.document_service import DocumentService
    from src.core import get_config
    
    config = get_config()
    service = DocumentService(config.config)
    
    import glob
    files = glob.glob(args.batch)
    
    if not files:
        logger.error(f"No files matched pattern: {args.batch}")
        return 1
    
    logger.info(f"Processing {len(files)} documents...")
    results = service.batch_process(files, args.type)
    
    logger.info(f"Batch ID: {results['batch_id']}")
    logger.info(f"Successful: {results['summary']['success_count']}")
    logger.info(f"Failed: {results['summary']['failed_count']}")
    
    if args.output:
        import json
        output_path = Path(args.output)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"Results saved to: {output_path}")
    
    return 0 if results['summary']['failed_count'] == 0 else 1


def search_documents(args) -> int:
    """Search processed documents."""
    from src.services.document_service import DocumentService
    from src.core import get_config
    
    config = get_config()
    service = DocumentService(config.config)
    
    results = service.search_documents(args.search, args.type)
    
    if not results:
        logger.info("No documents found matching search criteria.")
        return 1
    
    logger.info(f"\nFound {len(results)} document(s):")
    for doc in results:
        logger.info(f"  - {doc['document_id']}: {doc['metadata'].get('document_type', 'unknown')}")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
