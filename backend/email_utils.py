import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

GMAIL_EMAIL = os.getenv("GMAIL_EMAIL")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

def send_otp_email(to_email: str, otp: str):
    try:
        # Create email message
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your OTP Verification Code"
        message["From"] = GMAIL_EMAIL
        message["To"] = to_email
        
        # Email body
        text = f"""
Hello,

Your OTP code is: {otp}

This OTP is valid for a short time.
Do not share it with anyone.

Regards,
AI Chatbot Team
"""
        
        html = f"""
        <html>
            <body>
                <h2>Your OTP Verification Code</h2>
                <p>Hello,</p>
                <p>Your OTP code is: <strong>{otp}</strong></p>
                <p>This OTP is valid for a short time.</p>
                <p>Do not share it with anyone.</p>
                <p>Regards,<br>AI Chatbot Team</p>
            </body>
        </html>
        """
        
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)
        
        # Send email via Gmail SMTP
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            server.sendmail(GMAIL_EMAIL, to_email, message.as_string())
        
        print(f"Email sent successfully to {to_email}")
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        raise
