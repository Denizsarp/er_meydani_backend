import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
from fastapi import HTTPException, status

load_dotenv()

SMPT_SERVER = 'smtp.gmail.com'
SMTP_PORT = 465


class Email:
    def email_verification_send(email:str, code:str):
        sender_email = os.getenv('SENDER_EMAIL')
        sender_password = os.getenv('SENDER_PASSWORD')
        msg = EmailMessage()

        msg["Subject"] = "Verification Code"
        msg["From"] = sender_email
        msg["To"] = email
        msg.set_content(f"Hello your verification code: {code}. (this code will expire in 1 hour.)")

        try:
            with smtplib.SMTP(SMPT_SERVER, SMTP_PORT) as server:
                server.login(
                    sender_email,
                    sender_password
                )
                server.send_message(msg)
        except Exception as exc:
            raise HTTPException(detail="Email server error!", status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
        