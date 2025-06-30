import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from config.config import Config
import logging
from datetime import datetime
import os

logger = logging.getLogger(__name__)

class EmailSender:
    @staticmethod
    def send_email(subject, body, attachments=None):
        """
        Send email with the report
        
        Args:
            subject: Email subject
            body: Email body (HTML)
            attachments: List of file paths to attach
        """
        msg = MIMEMultipart()
        msg['From'] = Config.EMAIL_SENDER
        msg['To'] = ", ".join(Config.EMAIL_RECIPIENTS)
        msg['Subject'] = subject
        
        # Attach HTML body
        msg.attach(MIMEText(body, 'html'))
        
        # Attach files if any
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=os.path.basename(file_path)
                    )
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                msg.attach(part)
        
        try:
            with smtplib.SMTP(Config.EMAIL_SMTP_SERVER, Config.EMAIL_SMTP_PORT) as server:
                server.starttls()
                server.login(Config.EMAIL_SENDER, Config.EMAIl_SENDER_PASSWORD)
                server.sendmail(Config.EMAIL_SENDER, Config.EMAIL_RECIPIENTS, msg.as_string())
            logger.info("Email sent successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to send email: {str(e)}")
            return False