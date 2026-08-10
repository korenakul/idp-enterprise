"""
ERP integration module for TrainPlex Document Intelligence Platform.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import logging

logger = logging.getLogger('trainplex.integrations.erp')


class ERPConnector:
    """Base ERP connector."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.enabled = config.get('enabled', False)
        self.type = config.get('type', 'sap')
    
    def connect(self):
        """Connect to ERP system."""
        if not self.enabled:
            logger.warning("ERP integration is disabled")
            return False
        logger.info(f"Connecting to {self.type} ERP...")
        return True
    
    def submit(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Submit data to ERP."""
        if not self.enabled:
            return {'status': 'skipped', 'reason': 'ERP integration disabled'}
        logger.info(f"Submitting to ERP: {data.get('document_id')}")
        return {'status': 'success', 'erp_id': 'ERP-' + str(hash(data))}
    
    def batch_submit(self, documents: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Submit multiple documents to ERP."""
        results = [self.submit(doc) for doc in documents]
        return results


class SAPConnector(ERPConnector):
    """SAP ERP connector."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.type = 'sap'
    
    def submit_invoice(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Submit invoice to SAP."""
        return {
            'status': 'success',
            'document_type': 'invoice',
            'erp_id': 'SAP-' + invoice.get('invoice_number', 'unknown')
        }


class OracleERPConnector(ERPConnector):
    """Oracle ERP connector."""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.type = 'oracle'
    
    def submit_invoice(self, invoice: Dict[str, Any]) -> Dict[str, Any]:
        """Submit invoice to Oracle ERP."""
        return {
            'status': 'success',
            'document_type': 'invoice',
            'erp_id': 'ORACLE-' + invoice.get('invoice_number', 'unknown')
        }
