import os
from datetime import datetime, timedelta

class Config:
    # SAP Connection Parameters
    SAP_ASHOST = os.getenv('SAP_ASHOST', 'sap.server.com')  # SAP application server
    SAP_SYSNR = os.getenv('SAP_SYSNR', '00')                # SAP system number
    SAP_CLIENT = os.getenv('SAP_CLIENT', '100')             # SAP client
    SAP_USER = os.getenv('SAP_USER', 'RFC_USER')            # RFC user
    SAP_PASSWD = os.getenv('SAP_PASSWD', 'password')        # RFC password
    
    # Email Configuration
    EMAIL_SMTP_SERVER = os.getenv('EMAIL_SMTP_SERVER', 'smtp.company.com')
    EMAIL_SMTP_PORT = int(os.getenv('EMAIL_SMTP_PORT', 587))
    EMAIL_SENDER = os.getenv('EMAIL_SENDER', 'sap-reports@company.com')
    EMAIL_SENDER_PASSWORD = os.getenv('EMAIL_SENDER_PASSWORD', 'email_password')
    EMAIL_RECIPIENTS = os.getenv('EMAIL_RECIPIENTS', 'finance-team@company.com').split(',')
    
    # Report Configuration
    REPORT_DAYS_BACK = int(os.getenv('REPORT_DAYS_BACK', 1))  # Default: last 24 hours
    REPORT_TIMEZONE = os.getenv('REPORT_TIMEZONE', 'UTC')
    
    @staticmethod
    def get_date_range():
        """Get date range for the report (last 24 hours by default)"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=Config.REPORT_DAYS_BACK)
        return start_date.date(), end_date.date()