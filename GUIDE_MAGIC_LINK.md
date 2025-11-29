# 🔐 GUIDE MAGIC LINK - Implémentation

**Date :** 29 Novembre 2025  
**Objectif :** Connecter l'UI magic link existante au backend

---

## 🎯 Contexte

**CE QUI EXISTE DÉJÀ :**
- ✅ Frontend UI complète dans `sign-in-form.tsx`
- ✅ Formulaire email + états (magic/verify)
- ✅ Design moderne avec toast notifications

**CE QUI MANQUE :**
- ❌ Backend : Routes `/magic-link/send` et `/verify`
- ❌ Backend : Service email
- ❌ Frontend : Appel API réel (actuellement mock)

**TEMPS ESTIMÉ : 2h30**

---

## 📋 Plan d'Action

```
1. Backend : Service Email        (1h)
2. Backend : Routes Magic Link    (1h)
3. Frontend : Connection          (30min)
4. Test E2E                       (30min bonus)
```

---

## 🔧 PARTIE 1 : Backend Service Email

### Étape 1.1 : Créer la structure

```bash
cd /Users/michaelamar/Downloads/Avaai-main

# Créer le dossier email
mkdir -p api/src/infrastructure/email

# Créer les fichiers
touch api/src/infrastructure/email/__init__.py
touch api/src/infrastructure/email/email_service.py
```

### Étape 1.2 : Code du service email

**Fichier : `api/src/infrastructure/email/email_service.py`**

```python
"""
Service d'envoi d'emails pour l'authentification.
En mode dev (sans SMTP), les liens sont loggés dans la console.
"""
from __future__ import annotations

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from api.src.core.logging import app_logger


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
    
    async def send_magic_link(self, to_email: str, magic_token: str) -> bool:
        """
        Envoie un magic link pour authentification.
        
        Args:
            to_email: Email du destinataire
            magic_token: Token JWT pour vérification
            
        Returns:
            True si envoyé avec succès, False sinon
        """
        # URL complète du magic link
        magic_url = f"{self.frontend_url}/verify-magic-link?token={magic_token}"
        
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
            app_logger.error(f"Failed to send magic link to {to_email}: {e}")
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
            app_logger.warning("⚠️ SMTP not configured - DEV MODE")
            app_logger.info(f"""
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
                app_logger.info(f"🔗 MAGIC LINK URL: {url_match.group(1)}")
            
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
            
            app_logger.info(f"✅ Magic link sent successfully to {to_email}")
            return True
            
        except Exception as e:
            app_logger.error(f"❌ SMTP error sending to {to_email}: {e}")
            return False


# Singleton instance
_email_service: EmailService | None = None


def get_email_service() -> EmailService:
    """Get or create the email service singleton."""
    global _email_service
    if _email_service is None:
        _email_service = EmailService()
    return _email_service
```

### Étape 1.3 : Fichier `__init__.py`

**Fichier : `api/src/infrastructure/email/__init__.py`**

```python
"""Email infrastructure module."""
from api.src.infrastructure.email.email_service import EmailService, get_email_service

__all__ = ["EmailService", "get_email_service"]
```

---

## 🔧 PARTIE 2 : Backend Routes Magic Link

### Étape 2.1 : Modifier `auth.py`

**Fichier : `api/src/presentation/api/v1/routes/auth.py`**

**Ajouter ces imports en haut (si pas déjà présents) :**

```python
from datetime import datetime, timedelta
from pydantic import BaseModel, field_validator
from fastapi import HTTPException, status
from sqlalchemy import select
from api.src.infrastructure.email.email_service import get_email_service
from api.src.domain.entities.user import User
```

**Ajouter ce schema Pydantic (avant ou après les autres schemas) :**

```python
class MagicLinkRequest(BaseModel):
    """Request pour magic link."""
    email: str
    
    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        v = v.lower().strip()
        if "@" not in v or "." not in v.split("@")[1]:
            raise ValueError("Email invalide")
        return v
```

**Ajouter ces 2 routes à la fin du fichier (avant le dernier commentaire) :**

```python
@router.post("/magic-link/send")
async def send_magic_link(
    request: MagicLinkRequest,
    session: AsyncSession = Depends(get_session),
):
    """
    Envoie un magic link par email pour connexion sans password.
    
    Le token expire après 15 minutes.
    Pour la sécurité, retourne toujours succès même si l'email n'existe pas.
    """
    from api.src.core.security import create_access_token
    
    # Vérifier que l'user existe
    query = select(User).filter(User.email == request.email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    # Pour la sécurité : ne pas révéler si l'email existe
    # Toujours retourner le même message
    success_message = {
        "success": True,
        "message": "Si un compte existe avec cet email, un lien de connexion a été envoyé."
    }
    
    if not user:
        # Email n'existe pas, mais on ne le dit pas
        app_logger.info(f"Magic link requested for non-existent email: {request.email}")
        return success_message
    
    # Créer un token JWT de courte durée (15min)
    magic_token = create_access_token(
        data={
            "sub": user.email,
            "type": "magic_link",
            "user_id": str(user.id)
        },
        expires_delta=timedelta(minutes=15)
    )
    
    # Envoyer l'email
    email_service = get_email_service()
    email_sent = await email_service.send_magic_link(
        to_email=user.email,
        magic_token=magic_token
    )
    
    if not email_sent:
        # En dev sans SMTP, c'est OK (juste loggé)
        # En prod, c'est une vraie erreur
        if email_service.smtp_user and email_service.smtp_password:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Échec de l'envoi de l'email. Réessayez dans quelques instants."
            )
    
    return success_message


@router.get("/magic-link/verify")
async def verify_magic_link(
    token: str,
    session: AsyncSession = Depends(get_session),
):
    """
    Vérifie un magic link token et connecte l'utilisateur.
    
    Retourne access_token et refresh_token pour la session.
    """
    from api.src.core.security import verify_token, create_access_token, create_refresh_token
    
    # Vérifier le token
    try:
        payload = verify_token(token)
        
        # Vérifier que c'est bien un magic link token
        if payload.get("type") != "magic_link":
            raise ValueError("Not a magic link token")
        
        email = payload.get("sub")
        if not email:
            raise ValueError("Missing email in token")
        
    except Exception as e:
        app_logger.warning(f"Invalid magic link token: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lien de connexion invalide ou expiré"
        )
    
    # Récupérer l'utilisateur
    query = select(User).filter(User.email == email)
    result = await session.execute(query)
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur introuvable"
        )
    
    # Créer les tokens de session (longue durée)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": str(user.id)}
    )
    
    app_logger.info(f"✅ Magic link verified successfully for {user.email}")
    
    # Retourner les tokens + user info
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(user.id),
            "email": user.email,
            "name": user.name,
            "onboarding_completed": user.onboarding_completed or False,
        }
    }
```

---

## 🎨 PARTIE 3 : Frontend Connection

### Étape 3.1 : Modifier `sign-in-form.tsx`

**Fichier : `webapp/components/auth/sign-in-form.tsx`**

**Remplacer la fonction `handleMagicSubmit` (ligne ~48) :**

**AVANT (mock) :**
```typescript
const handleMagicSubmit = async (values: SignInValues) => {
  setEmail(values.email);
  toast(t("magic.success", { defaultValue: "Magic link sent! Check your inbox." }), {
    description: values.email,
  });
  setTimeout(() => setStep("verify"), 400);
};
```

**APRÈS (vrai appel API) :**
```typescript
const [isLoading, setIsLoading] = useState(false); // Ajouter cet état en haut du composant

const handleMagicSubmit = async (values: SignInValues) => {
  setIsLoading(true);
  
  try {
    // Appel API backend
    const response = await fetch('/api/auth/magic-link/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: values.email }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.detail || 'Erreur lors de l\'envoi');
    }
    
    // Succès
    setEmail(values.email);
    toast.success(
      t("magic.success", { defaultValue: "Magic link sent! Check your inbox." }), 
      { description: values.email }
    );
    setTimeout(() => setStep("verify"), 400);
    
  } catch (error) {
    console.error('Magic link error:', error);
    toast.error(
      t("magic.error", { defaultValue: "Failed to send magic link" }), 
      { description: error instanceof Error ? error.message : "Please try again" }
    );
  } finally {
    setIsLoading(false);
  }
};
```

**Et modifier le bouton submit pour utiliser `isLoading` :**

```typescript
<Button type="submit" size="lg" className="w-full" disabled={isLoading}>
  {isLoading 
    ? t("cta.sending", { defaultValue: "Sending..." })
    : t("cta.magic", { defaultValue: "Send magic link" })
  }
</Button>
```

### Étape 3.2 : Créer route Next.js API

**Fichier : `webapp/app/api/auth/magic-link/send/route.ts`** (à créer)

```bash
mkdir -p webapp/app/api/auth/magic-link/send
touch webapp/app/api/auth/magic-link/send/route.ts
```

**Contenu :**

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json();
    
    // Forward request to FastAPI backend
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    const response = await fetch(`${backendUrl}/api/v1/auth/magic-link/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email }),
    });
    
    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
    
  } catch (error) {
    console.error('Magic link proxy error:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

### Étape 3.3 : Créer route verify (optionnel)

**Fichier : `webapp/app/api/auth/magic-link/verify/route.ts`** (à créer)

```bash
mkdir -p webapp/app/api/auth/magic-link/verify
touch webapp/app/api/auth/magic-link/verify/route.ts
```

```typescript
import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    const token = request.nextUrl.searchParams.get('token');
    
    if (!token) {
      return NextResponse.json(
        { detail: 'Token missing' },
        { status: 400 }
      );
    }
    
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    
    const response = await fetch(
      `${backendUrl}/api/v1/auth/magic-link/verify?token=${token}`
    );
    
    const data = await response.json();
    
    return NextResponse.json(data, { status: response.status });
    
  } catch (error) {
    console.error('Magic link verify error:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

---

## ✅ PARTIE 4 : Test Complet

### Test Manuel (5 min)

```bash
# 1. Lancer le backend
cd /Users/michaelamar/Downloads/Avaai-main
source .venv/bin/activate
cd api
uvicorn api.main:app --reload --port 8000

# 2. Dans un autre terminal, lancer le frontend
cd /Users/michaelamar/Downloads/Avaai-main/webapp
npm run dev

# 3. Ouvrir le navigateur
open http://localhost:3000/login

# 4. Flow de test:
# - Cliquer sur "Continue with magic link" (si bouton dédié)
# - OU entrer email et voir le bouton "Send magic link"
# - Cliquer le bouton
# - Vérifier les logs backend → copier le magic link
# - Ouvrir le lien dans le navigateur
# - Devrait être connecté et redirigé vers /dashboard
```

### Vérifier les Logs Backend

Chercher dans la console backend :
```
╔══════════════════════════════════════════════════════════════
║ 📧 MAGIC LINK (DEV MODE)
╠══════════════════════════════════════════════════════════════
║ To: test@example.com
║ Subject: 🔐 Connexion à AvaFirst AI
║
║ ✉️ Check the HTML body above for the magic link URL
╚══════════════════════════════════════════════════════════════

🔗 MAGIC LINK URL: http://localhost:3000/verify-magic-link?token=eyJhb...
```

**Copier cette URL et l'ouvrir !**

---

## 🧪 Test Automatisé (Bonus)

**Fichier : `api/tests/test_magic_link.py`** (à créer)

```python
"""Tests for magic link authentication."""
import pytest
from fastapi import status


@pytest.mark.asyncio
async def test_send_magic_link_success(client_with_mock_user):
    """Test sending magic link with valid email."""
    response = client_with_mock_user.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "test@example.com"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert "lien de connexion" in data["message"].lower()


@pytest.mark.asyncio
async def test_send_magic_link_invalid_email(client):
    """Test sending magic link with invalid email format."""
    response = client.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "not-an-email"}
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_verify_magic_link_invalid_token(client):
    """Test verifying with invalid token."""
    response = client.get("/api/v1/auth/magic-link/verify?token=invalid")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "invalide" in response.json()["detail"].lower()
```

**Lancer le test :**
```bash
python -m pytest api/tests/test_magic_link.py -v
```

---

## ✅ Checklist Finale

### Backend
- [ ] ✅ `email_service.py` créé et fonctionne en mode dev
- [ ] ✅ Route `/magic-link/send` implémentée
- [ ] ✅ Route `/magic-link/verify` implémentée
- [ ] ✅ Logs clairs en mode dev (URL visible)
- [ ] ✅ Tests unitaires créés

### Frontend
- [ ] ✅ `sign-in-form.tsx` modifié (appel API réel)
- [ ] ✅ Route Next.js `/api/auth/magic-link/send` créée
- [ ] ✅ Route Next.js `/api/auth/magic-link/verify` créée (optionnel)
- [ ] ✅ Loading states ajoutés
- [ ] ✅ Error handling avec toast

### Tests
- [ ] ✅ Test manuel : Email → Magic Link → Login ✅
- [ ] ✅ Tests automatisés passent
- [ ] ✅ Vérifier logs backend (URL visible en dev)

---

## 🎉 Résultat Attendu

**Après cette implémentation :**

1. User entre son email sur `/login`
2. Clique "Send magic link"
3. Backend génère JWT token (15min)
4. Email service log l'URL (en dev)
5. User copie l'URL depuis les logs
6. User clique l'URL → vérifie token
7. Backend retourne access_token + refresh_token
8. Frontend sauvegarde tokens
9. User redirigé vers `/dashboard` ✅

**MAGIC LINK COMPLET FONCTIONNEL !** 🚀

---

## 🔧 Configuration SMTP (Production)

**Pour envoyer de vrais emails, ajouter dans `.env` :**

```bash
# Gmail example
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=votre-email@gmail.com
SMTP_PASSWORD=votre-app-password
FROM_EMAIL=noreply@avafirst.ai

# Frontend URL
FRONTEND_URL=https://votre-domaine.com
```

**Note Gmail :** Utiliser un "App Password", pas votre password Gmail direct.

---

*Guide créé le : 29 novembre 2025*

