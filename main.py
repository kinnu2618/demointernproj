import logging
from datetime import datetime
from config.config import Config
from sap.rfc_client import SAPRFCClient
from utils.email_sender import EmailSender
from jinja2 import Template
import csv
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def generate_report(payments, start_date, end_date):
    """Generate HTML report and CSV file"""
    # Calculate totals
    total_amount = sum(p['amount'] for p in payments) if payments else 0
    currency = payments[0]['currency'] if payments else ''
    count = len(payments) if payments else 0
    
    # Render HTML email
    with open('config/email_template.html', 'r') as f:
        template = Template(f.read())
    
    html_content = template.render(
        payments=payments,
        start_date=start_date,
        end_date=end_date,
        total_amount=total_amount,
        currency=currency,
        count=count
    )
    
    # Generate CSV file
    csv_filename = f"vendor_payments_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    if payments:
        with open(csv_filename, 'w', newline='') as csvfile:
            fieldnames = payments[0].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(payments)
    
    return html_content, csv_filename if payments else None

def main():
    logger.info("Starting SAP Vendor Payments Report")
    
    # Get date range from config
    start_date, end_date = Config.get_date_range()
    logger.info(f"Fetching vendor payments from {start_date} to {end_date}")
    
    # Connect to SAP and fetch data
    sap_client = SAPRFCClient()
    payments = sap_client.get_vendor_payments(start_date, end_date)
    sap_client.disconnect()
    
    if payments is None:
        logger.error("Failed to retrieve vendor payments from SAP")
        return
    
    logger.info(f"Retrieved {len(payments)} vendor payments")
    
    # Generate report and email
    html_content, csv_filename = generate_report(payments, start_date, end_date)
    
    subject = f"Daily Vendor Payments Report - {end_date.strftime('%Y-%m-%d')}"
    attachments = [csv_filename] if csv_filename else None
    
    # Send email
    email_sent = EmailSender.send_email(subject, html_content, attachments)
    
    # Clean up
    if csv_filename and os.path.exists(csv_filename):
        os.remove(csv_filename)
    
    logger.info("SAP Vendor Payments Report completed")

if __name__ == "__main__":
    main()