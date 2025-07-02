import logging
from datetime import datetime
from pathlib import Path
from lib.sap_connector import SAPConnector
from lib.email_sender import EmailSender
from config.config import REPORT_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(REPORT_CONFIG['output_dir'] / 'payment_report.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def main():
    logger.info("Starting SAP Vendor Payments Report process")
    
    try:
        # Step 1: Connect to SAP and fetch data
        sap_connector = SAPConnector()
        sap_connector.connect()
        
        payment_data = sap_connector.get_vendor_payments()
        
        if payment_data is None or payment_data.empty:
            logger.info("No payment data to process. Exiting.")
            return
        
        # Step 2: Save data to CSV
        csv_file = sap_connector.save_to_csv(payment_data)
        
        # Step 3: Prepare and send email
        email_sender = EmailSender()
        email_content = email_sender.create_email_content(payment_data)
        
        email_subject = f"Vendor Payments {datetime.now().strftime('%Y-%m-%d')}"
        email_sender.send_email(email_subject, email_content, csv_file)
        
        logger.info("Process completed successfully")
        
    except Exception as e:
        logger.error(f"Process failed: {e}")
        raise
    finally:
        if 'sap_connector' in locals():
            sap_connector.disconnect()

if __name__ == "__main__":
    main()