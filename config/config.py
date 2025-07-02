import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- SAP Connection Configuration ---
SAP_CONFIG = {
    'user': os.getenv('SAP_USER'),
    'passwd': os.getenv('SAP_PASSWORD'),
    'ashost': os.getenv('SAP_HOST'),
    'sysnr': os.getenv('SAP_SYSTEM_NUMBER', '00'),
    'client': os.getenv('SAP_CLIENT', '100'),
    'lang': os.getenv('SAP_LANGUAGE', 'EN'),
}

# --- Email Configuration ---
EMAIL_CONFIG = {
    'smtp_server': os.getenv('SMTP_SERVER'),
    'smtp_port': int(os.getenv('SMTP_PORT', '587')),
    'smtp_user': os.getenv('SMTP_USER'),
    'smtp_password': os.getenv('SMTP_PASSWORD'),
    'sender_email': os.getenv('SENDER_EMAIL'),
    'recipients': [
        email.strip()
        for email in os.getenv('RECIPIENT_EMAILS', '').split(',') if email.strip()
    ],
    'subject_prefix': os.getenv('EMAIL_SUBJECT_PREFIX', 'SAP Vendor Payments Report - '),
}

# --- Report Configuration ---
REPORT_CONFIG = {
    'output_dir': Path(os.getenv('OUTPUT_DIR', 'data')),
    'days_back': int(os.getenv('DAYS_BACK', '1')),
    'function_module': os.getenv('SAP_FUNCTION_MODULE', 'BAPI_ACC_DOCUMENT_GETLIST'),
    'company_code': os.getenv('COMPANY_CODE', '1000'),
}

# Ensure the output directory exists
REPORT_CONFIG['output_dir'].mkdir(parents=True, exist_ok=True)

