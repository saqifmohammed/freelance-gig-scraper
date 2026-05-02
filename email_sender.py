import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from config import config
from scrapers import Job
import os


class EmailSender:
    def __init__(self):
        self.smtp_server = config.smtp_server
        self.smtp_port = config.smtp_port
        self.sender_email = config.sender_email
        self.sender_password = config.sender_password
        self.recipient_email = config.recipient_email

    def send_excel_report(self, excel_filepath: str, job_count: int) -> bool:
        if not os.path.exists(excel_filepath):
            print("Excel file not found")
            return False

        subject = f"AI Job Leads - {datetime.now().strftime('%Y-%m-%d %H:%M')} - {job_count} opportunities"

        body = f"""Hi,

Here's your weekly AI job leads report.

Total Jobs Found: {job_count}

The Excel file contains detailed information for each job including:
- Platform
- Job Title
- Description
- Budget
- URL
- Posted Date

Each run creates a new sheet in the Excel file.

Run Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Best regards,
AI Job Leads Automation
"""

        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg.attach(MIMEText(body, 'plain'))

        try:
            with open(excel_filepath, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(excel_filepath)}"
            )
            msg.attach(part)

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            print(f"Email sent successfully with {job_count} jobs")
            return True
        except Exception as e:
            print(f"Email send error: {e}")
            return False

    def send_jobs_report(self, jobs: list[Job]) -> bool:
        return self.send_excel_report("", len(jobs))