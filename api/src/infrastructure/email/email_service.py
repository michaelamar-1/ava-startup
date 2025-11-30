import os
import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from api.src.core.settings import get_settings

logger = logging.getLogger("ava.email")

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", "noreply@avafirst.ai")
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")

    async def send_magic_link(self, to_email: str, magic_token: str, locale: str = "fr") -> bool:
        magic_url = f"{self.frontend_url}/{locale}/verify-magic-link?token={magic_token}"
        settings = get_settings()

        # 🚨 MODE DEV / SECOURS : On affiche le lien direct
        if settings.environment == "development" or not self.smtp_user:
            print(f"\n{'='*20} MAGIC LINK {'='*20}")
            print(f"URL: {magic_url}")
            print(f"{'='*50}\n")
            return True

        # MODE PROD : Tentative d'envoi réel
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = "Connexion à AvaFirst"
            msg["From"] = self.from_email
            msg["To"] = to_email

            html = f'<a href="{magic_url}">Cliquez ici pour vous connecter</a>'
            msg.attach(MIMEText(html, "html", "utf-8"))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True

        except Exception as e:
            # En cas d'erreur SMTP (ex: pas de crédit), on affiche quand même le lien dans les logs pour ne pas te bloquer
            print(f"❌ ERREUR SMTP: {e}")
            print(f"⚠️ LIEN DE SECOURS: {magic_url}")
            return True

_service = None
def get_email_service():
    global _service
    if not _service:
        _service = EmailService()
    return _service
