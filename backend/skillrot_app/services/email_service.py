import os
import base64
import requests
from skillrot_app.core.config import settings


SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
FROM_EMAIL = settings.EMAIL_ADDRESS


def send_email(to_email: str, subject: str, html_body: str, text_body: str = None) -> bool:
    try:
        if not SENDGRID_API_KEY:
            print("SendGrid API key missing.")
            return False

        data = {
            "personalizations": [
                {
                    "to": [{"email": to_email}],
                    "subject": subject
                }
            ],
            "from": {
                "email": FROM_EMAIL,
                "name": "SkillDelta Alerts"
            },
            "reply_to": {
                "email": "noreply@skilldelta.com",
                "name": "SkillDelta No-Reply"
            },
            "content": [
                {
                    "type": "text/plain",
                    "value": text_body or "Please view this email in a client that supports HTML."
                },
                {
                    "type": "text/html",
                    "value": html_body
                }
            ]
        }

        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={
                "Authorization": f"Bearer {SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            },
            json=data,
            timeout=15
        )

        if response.status_code in [200, 202]:
            print("SkillDelta Email sent via SendGrid.")
            return True
        else:
            print("SendGrid Error:", response.text)
            return False

    except Exception as e:
        print("SendGrid Exception:", str(e))
        return False
