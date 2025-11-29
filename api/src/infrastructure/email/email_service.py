"""
Service d'envoi d'emails pour l'authentification.
En mode dev (sans SMTP), les liens sont loggés dans la console.
"""
from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import logging

logger = logging.getLogger("ava.email")


class EmailService:
    """Service pour envoyer des emails via SMTP."""
    
    def __init__(
        self,
        smtp_host: str | None = None,
        smtp_port: int | None = None,
        smtp_user: str | None = None,
        smtp_password: str | None = None,
    ):
        """Initialize email service with SMTP credentials."""
        from api.src.core.settings import get_settings
        settings = get_settings()
        
        # Config SMTP (depuis env ou paramètres)
        self.smtp_host = smtp_host or os.getenv("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = smtp_port or int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = smtp_user or os.getenv("SMTP_USER", "")
        self.smtp_password = smtp_password or os.getenv("SMTP_PASSWORD", "")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user or "noreply@avafirst.ai")
        
        # URL frontend pour le magic link
        self.frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    async def send_magic_link(self, to_email: str, magic_token: str, locale: str = "fr") -> bool:
        """
        Envoie un magic link pour authentification.
        
        Args:
            to_email: Email du destinataire
            magic_token: Token JWT pour vérification
            locale: Langue de l'utilisateur (fr, en, he)
            
        Returns:
            True si envoyé avec succès, False sinon
        """
        # URL complète du magic link (avec locale)
        magic_url = f"{self.frontend_url}/{locale}/verify-magic-link?token={magic_token}"
        
        subject = "🔐 Connexion à AvaFirst AI"
        
        # Email HTML (beau design)
        html_body = self._create_html_email(to_email, magic_url)
        
        # Email texte (fallback)
        text_body = f"""
Connexion à AvaFirst AI

Bonjour !

Cliquez sur ce lien pour vous connecter :
{magic_url}

⏱️ Ce lien expire dans 15 minutes.

Si vous n'avez pas demandé cette connexion, ignorez cet email.

---
AvaFirst AI - Votre réceptionniste IA
        """.strip()
        
        try:
            return await self._send_email(to_email, subject, html_body, text_body)
        except Exception as e:
            logger.error(f"Failed to send magic link to {to_email}: {e}")
            return False
    
    def _create_html_email(self, to_email: str, magic_url: str) -> str:
        """Crée l'email HTML avec design moderne."""
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }}
        .container {{
            max-width: 600px;
            margin: 40px auto;
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        .header {{
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            padding: 40px 30px;
            text-align: center;
            color: white;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 600;
        }}
        .content {{
            padding: 40px 30px;
        }}
        .button {{
            display: inline-block;
            padding: 16px 32px;
            background: #6366f1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            margin: 20px 0;
            transition: background 0.3s;
        }}
        .button:hover {{
            background: #4f46e5;
        }}
        .link-box {{
            background: #f9fafb;
            padding: 16px;
            border-radius: 8px;
            word-break: break-all;
            font-size: 14px;
            color: #6b7280;
            margin: 20px 0;
        }}
        .footer {{
            background: #f9fafb;
            padding: 30px;
            text-align: center;
            font-size: 12px;
            color: #6b7280;
            border-top: 1px solid #e5e7eb;
        }}
        .warning {{
            background: #fef3c7;
            border-left: 4px solid #f59e0b;
            padding: 12px 16px;
            margin: 20px 0;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AvaFirst AI</h1>
        </div>
        
        <div class="content">
            <h2>Connexion à votre compte</h2>
            <p>Bonjour !</p>
            <p>Vous avez demandé un lien de connexion pour accéder à votre compte AvaFirst AI.</p>
            
            <div style="text-align: center;">
                <a href="{magic_url}" class="button">
                    🔓 Se connecter maintenant
                </a>
            </div>
            
            <p style="margin-top: 30px;">Ou copiez-collez ce lien dans votre navigateur :</p>
            <div class="link-box">
                {magic_url}
            </div>
            
            <div class="warning">
                <strong>⏱️ Attention :</strong> Ce lien expire dans 15 minutes pour votre sécurité.
            </div>
            
            <p style="margin-top: 30px; font-size: 14px; color: #6b7280;">
                Si vous n'avez pas demandé cette connexion, ignorez cet email en toute sécurité.
            </p>
        </div>
        
        <div class="footer">
            <p><strong>AvaFirst AI</strong></p>
            <p>Votre réceptionniste téléphonique intelligent</p>
            <p style="margin-top: 16px;">
                © 2025 AvaFirst AI - Tous droits réservés
            </p>
        </div>
    </div>
</body>
</html>
        """.strip()
    
    async def _send_email(
        self,
        to_email: str,
        subject: str,
        html_body: str,
        text_body: str,
    ) -> bool:
        """Envoie un email via SMTP."""
        
        # MODE DEV : Si pas de config SMTP, juste logger
        if not self.smtp_user or not self.smtp_password:
            logger.warning("⚠️ SMTP not configured - DEV MODE")
            logger.info(f"""
╔══════════════════════════════════════════════════════════════
║ 📧 MAGIC LINK (DEV MODE)
╠══════════════════════════════════════════════════════════════
║ To: {to_email}
║ Subject: {subject}
║
║ ✉️ Check the HTML body above for the magic link URL
║ (In production, this would be sent via SMTP)
╚══════════════════════════════════════════════════════════════
            """)
            # Extraire et logger juste l'URL pour facilité
            import re
            url_match = re.search(r'(http[s]?://[^\s<>"]+)', html_body)
            if url_match:
                logger.info(f"🔗 MAGIC LINK URL: {url_match.group(1)}")
            
            return True  # Considéré succès en dev
        
        # MODE PRODUCTION : Envoyer vraiment via SMTP
        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = self.from_email
            msg["To"] = to_email
            
            # Attacher texte et HTML
            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))
            
            # Envoyer via SMTP
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"✅ Magic link sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ SMTP error sending to {to_email}: {e}")
            return False


# Singleton instance
_email_service: EmailService | None = None


def get_email_service() -> EmailService:
    """Get or create the email service singleton."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
