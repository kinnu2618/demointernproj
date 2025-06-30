from pyrfc import Connection, ABAPApplicationError, ABAPRuntimeError, LogonError, CommunicationError
from config.config import Config
from datetime import date
import logging

logger = logging.getLogger(__name__)

class SAPRFCClient:
    def __init__(self):
        self.connection = None
        
    def connect(self):
        """Establish connection to SAP system"""
        try:
            self.connection = Connection(
                ashost=Config.SAP_ASHOST,
                sysnr=Config.SAP_SYSNR,
                client=Config.SAP_CLIENT,
                user=Config.SAP_USER,
                passwd=Config.SAP_PASSWD
            )
            logger.info("Successfully connected to SAP system")
            return True
        except CommunicationError:
            logger.error("Could not connect to SAP server")
        except LogonError:
            logger.error("Could not log in to SAP system - check credentials")
        except Exception as e:
            logger.error(f"Unknown error connecting to SAP: {str(e)}")
        return False
    
    def disconnect(self):
        """Close SAP connection"""
        if self.connection:
            self.connection.close()
            logger.info("Disconnected from SAP system")
    
    def get_vendor_payments(self, start_date: date, end_date: date):
        """
        Retrieve vendor payments within date range using BAPI
        
        Args:
            start_date: Start date for payment documents
            end_date: End date for payment documents
            
        Returns:
            List of payment documents or None if error occurs
        """
        if not self.connection:
            if not self.connect():
                return None
                
        try:
            # First get list of accounting documents in date range
            doc_list = self.connection.call(
                'BAPI_ACC_DOCUMENT_GETLIST',
                POSTINGDATE_FROM=start_date.isoformat(),
                POSTINGDATE_TO=end_date.isoformat(),
                DOCUMENTTYPE='KR'  # Vendor payment documents
            )
            
            payments = []
            
            # For each document, get details
            for doc in doc_list.get('DOCUMENT_LIST', []):
                doc_detail = self.connection.call(
                    'BAPI_ACC_DOCUMENT_GETDETAIL',
                    DOCUMENTNUMBER=doc['DOC_NO'],
                    FISCALYEAR=doc['FISC_YEAR'],
                    DOCUMENTTYPE=doc['DOC_TYPE']
                )
                
                # Extract payment information
                for item in doc_detail.get('ITEM_LIST', []):
                    if item['GL_ACCOUNT'].startswith('21'):  # Vendor accounts typically start with 21
                        payment = {
                            'document_number': doc['DOC_NO'],
                            'fiscal_year': doc['FISC_YEAR'],
                            'posting_date': doc['PSTNG_DATE'],
                            'vendor': item['VENDOR_NO'] if 'VENDOR_NO' in item else '',
                            'amount': item['AMT_DOCCUR'] if 'AMT_DOCCUR' in item else 0,
                            'currency': item['CURRENCY'] if 'CURRENCY' in item else '',
                            'text': item['ITEM_TEXT'] if 'ITEM_TEXT' in item else ''
                        }
                        payments.append(payment)
            
            return payments
            
        except ABAPApplicationError as e:
            logger.error(f"SAP application error: {str(e)}")
        except ABAPRuntimeError as e:
            logger.error(f"SAP runtime error: {str(e)}")
        except CommunicationError as e:
            logger.error(f"Communication error: {str(e)}")
        except Exception as e:
            logger.error(f"Unknown error fetching vendor payments: {str(e)}")
            
        return None