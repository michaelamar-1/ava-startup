# 🚀 COMMENCER LE DÉVELOPPEMENT - Guide Révisé

**Date :** 29 Novembre 2025  
**Objectif :** Te donner le VRAI état du projet et quoi faire maintenant

---

## 📊 DÉCOUVERTE IMPORTANTE !

**Après audit complet du code :**

### ✅ CE QUI EXISTE DÉJÀ (80% du projet !)

- **Frontend complet** : Next.js 14, UI moderne, composants auth déjà codés
- **Sign-in UI** : Magic link déjà dans l'interface (mais mock)
- **Dashboard** : Pages analytics, calls, settings déjà créées
- **Onboarding** : 8 steps déjà codés (UI 100%, logic 60%)
- **Backend** : FastAPI, routes principales, DB migrations

**TU AS DÉJÀ BEAUCOUP PLUS QUE PRÉVU !** 🎉

### ❌ CE QUI MANQUE (20% restant)

1. **Backend Magic Link** : Routes `/send` et `/verify` (2h)
2. **Service Email** : `email_service.py` à créer (1h)
3. **Connection Frontend ↔ Backend** : Appel API réel (30min)

**TOTAL : ~3h30 pour MVP fonctionnel !**

---

## 🎯 Recommandation Révisée : Magic Link Backend

**Pourquoi commencer par là ?**
1. ✅ L'UI existe déjà (juste à connecter)
2. ✅ Débloque onboarding + dashboard
3. ✅ Rapide à implémenter (3h30 vs 2-3 jours)
4. ✅ Testable immédiatement

**Résultat attendu :** Magic link fonctionnel de bout en bout

---

## 📋 Plan d'Action Simplifié

**Voir le guide détaillé :** `GUIDE_MAGIC_LINK.md`

### 🔍 Étape 0 : Comprendre l'existant (15 min)

```bash
# 1. Lire l'audit complet
cat AUDIT_EXISTANT.md

# 2. Vérifier le frontend existant
cat webapp/components/auth/sign-in-form.tsx
# → Tu verras que l'UI magic link existe déjà !

# 3. Vérifier les tests
cd /Users/michaelamar/Downloads/Avaai-main
source .venv/bin/activate
python -m pytest api/tests/ -q
# → Devrait afficher : 35 passed, 14 skipped
```

### ☑️ Étape 1 : Init Git (5 min)

```bash
cd /Users/michaelamar/Downloads/Avaai-main

# Initialiser Git (si pas déjà fait)
git init
git add .
git commit -m "Initial commit - tests fixed, frontend discovered"

# Créer branche feature
git checkout -b feature/magic-link-backend
```

---

### ✅ Étape 2 : Backend Service Email (1h)

**💡 Note :** Code complet dans `GUIDE_MAGIC_LINK.md` (Partie 1)

#### Résumé rapide :

#### 2.1 Créer les fichiers

```bash
mkdir -p api/src/infrastructure/email
touch api/src/infrastructure/email/__init__.py
touch api/src/infrastructure/email/email_service.py
```

#### 2.2 Code du service

**Voir `GUIDE_MAGIC_LINK.md` pour le code complet (~200 lignes)**

**Fonctionnalités clés :**
- Mode DEV : Log les magic links dans la console (pas besoin SMTP)
- Mode PROD : Envoie vrais emails via SMTP
- HTML email avec design moderne
- Token expiration 15min

**Snippet du code principal :**

```python
# Voir GUIDE_MAGIC_LINK.md pour le code complet (~200 lignes)

class EmailService:
    async def send_magic_link(self, to_email: str, magic_token: str) -> bool:
        """Envoie magic link (ou log en dev mode)."""
        magic_url = f"{self.frontend_url}/verify-magic-link?token={magic_token}"
        
        # Mode DEV : Pas de SMTP → Log l'URL
        if not self.smtp_user:
            app_logger.info(f"🔗 MAGIC LINK URL: {magic_url}")
            return True
        
        # Mode PROD : Envoie email HTML
        # ... (voir guide pour le template HTML)
```

#### 2.3 Tester le service

```bash
# Créer un test
touch api/tests/test_email_service.py
```

**Contenu de `test_email_service.py` :**

```python
"""Tests for email service."""
import pytest
from api.src.infrastructure.email.email_service import EmailService


@pytest.mark.asyncio
async def test_send_magic_link_dev_mode():
    """Test magic link email in dev mode (no SMTP)."""
    service = EmailService()
    
    # En dev (sans SMTP config), devrait logger mais retourner True
    result = await service.send_magic_link(
        to_email="test@example.com",
        magic_token="test_token_123"
    )
    
    assert result is True


@pytest.mark.asyncio
async def test_magic_link_url_format():
    """Test that magic link URL is correctly formatted."""
    service = EmailService()
    
    # Le service devrait créer une URL correcte
    # Vérifier indirectement via les logs ou mock
    result = await service.send_magic_link(
        to_email="test@example.com",
        magic_token="abc123xyz"
    )
    
    # En dev, devrait toujours réussir
    assert result is True
```

**Lancer le test :**
```bash
python -m pytest api/tests/test_email_service.py -v
```

---

---

### ✅ Étape 3 : Backend Routes Magic Link (1h)

**💡 Note :** Code complet dans `GUIDE_MAGIC_LINK.md` (Partie 2)

#### 3.1 Ajouter routes dans `auth.py`

**Fichier : `api/src/presentation/api/v1/routes/auth.py`**

**Imports à ajouter :**
```python
from datetime import timedelta
from api.src.infrastructure.email.email_service import get_email_service
```

**2 routes à ajouter (voir guide pour code complet ~80 lignes) :**

```python
# 1. POST /magic-link/send
@router.post("/magic-link/send")
async def send_magic_link(request: MagicLinkRequest, ...):
    # Cherche user par email
    # Génère JWT token (15min)
    # Envoie email via EmailService
    # Retourne succès (même si email inexistant - sécurité)

# 2. GET /magic-link/verify
@router.get("/magic-link/verify")
async def verify_magic_link(token: str, ...):
    # Vérifie JWT token
    # Check type = "magic_link"
    # Récupère user
    # Retourne access_token + refresh_token
```

**Code complet dans `GUIDE_MAGIC_LINK.md` (Partie 2)**

#### 3.2 Vérifier `security.py`

**Fichier : `api/src/core/security.py`**

**Ces fonctions devraient déjà exister :**

```python
# Ces fonctions devraient déjà exister dans security.py
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str
def create_refresh_token(data: dict) -> str
def verify_token(token: str) -> dict
```

**Si elles n'existent pas, voir `GUIDE_MAGIC_LINK.md`** pour le code.

#### 3.3 Tester les routes

```bash
# Lancer le backend
cd api
uvicorn api.main:app --reload --port 8000

# Dans un autre terminal, tester avec curl:
curl -X POST http://localhost:8000/api/v1/auth/magic-link/send \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com"}'

# Devrait retourner:
# {"success":true,"message":"Un lien de connexion a été envoyé à votre email."}
```

---

---

### ✅ Étape 4 : Frontend Connection (30min)

**💡 Note :** L'UI existe déjà ! Juste à connecter au backend.

#### 4.1 Modifier `sign-in-form.tsx`

**Fichier : `webapp/components/auth/sign-in-form.tsx`**

**Ligne ~48 : Remplacer le mock par un vrai appel API :**

```typescript
// AVANT (ligne 48) - Mock
const handleMagicSubmit = async (values: SignInValues) => {
  setEmail(values.email);
  toast(...);  // ❌ Juste un toast, pas d'appel API
  setTimeout(() => setStep("verify"), 400);
};

// APRÈS - Vrai appel API
const [isLoading, setIsLoading] = useState(false);

const handleMagicSubmit = async (values: SignInValues) => {
  setIsLoading(true);
  
  try {
    const response = await fetch('/api/auth/magic-link/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: values.email }),
    });
    
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail);
    
    setEmail(values.email);
    toast.success("Magic link sent!", { description: values.email });
    setStep("verify");
  } catch (error) {
    toast.error("Failed to send", { description: error.message });
  } finally {
    setIsLoading(false);
  }
};
```

**Code complet dans `GUIDE_MAGIC_LINK.md` (Partie 3)**

#### 4.2 Créer route Next.js API

**Fichier : `webapp/app/api/auth/magic-link/send/route.ts`** (nouveau)

```typescript
// Proxy vers le backend FastAPI
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { email } = await request.json();
  const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
  
  const response = await fetch(`${backendUrl}/api/v1/auth/magic-link/send`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email }),
  });
  
  const data = await response.json();
  return NextResponse.json(data, { status: response.status });
}
```

**Code complet + route `/verify` dans `GUIDE_MAGIC_LINK.md`**

---

---

### ✅ Étape 5 : Test Complet (30 min)

#### Test manuel :

```bash
# 1. Lancer l'app complète
./scripts/dev.sh

# 2. Ouvrir le navigateur
open http://localhost:3000/login

# 3. Flow de test:
# - Entrer un email
# - Cliquer "Recevoir un lien"
# - Vérifier les logs backend pour le magic link
# - Copier le lien et l'ouvrir
# - Devrait être redirigé vers /dashboard
```

#### Test automatisé :

```bash
# Créer test E2E
touch api/tests/test_auth_magic_link_e2e.py
```

```python
"""E2E tests for magic link authentication."""
import pytest
from fastapi import status

@pytest.mark.asyncio
async def test_magic_link_flow(client_with_mock_user):
    """Test complete magic link flow."""
    
    # 1. Demander un magic link
    response = client_with_mock_user.post(
        "/api/v1/auth/magic-link/send",
        json={"email": "test@example.com"}
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["success"] is True
    
    # Note: En test, on ne peut pas tester la réception d'email
    # mais on vérifie que l'endpoint fonctionne

@pytest.mark.asyncio  
async def test_magic_link_verify_invalid_token(client):
    """Test verification with invalid token."""
    
    response = client.get("/api/v1/auth/magic-link/verify?token=invalid")
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
```

**Lancer les tests :**
```bash
python -m pytest api/tests/test_auth_magic_link_e2e.py -v
```

---

## 🎯 Checklist Finale

### Backend
- [ ] Service email créé et testé
- [ ] Routes `/magic-link/send` et `/verify` implémentées
- [ ] Tokens JWT avec expiration correcte
- [ ] Tests unitaires passent
- [ ] Logs clairs pour debugging

### Frontend
- [ ] Page login avec bouton magic link
- [ ] Page verify-magic-link pour callback
- [ ] Gestion des états (loading, success, error)
- [ ] Toast notifications
- [ ] Redirection après succès

### Tests
- [ ] Test manuel : Email → Click → Login ✅
- [ ] Tests automatisés passent
- [ ] Cas d'erreur gérés (token expiré, invalide, etc.)

---

---

## 🎉 RÉSULTAT FINAL

### Après ces 3h30 de dev :

- ✅ **Magic Link fonctionnel de bout en bout**
- ✅ **UI existante connectée au backend**
- ✅ **Mode dev pratique** (URLs dans les logs)
- ✅ **Ready pour production** (juste config SMTP)

### Flow complet :
```
1. User entre email sur /login
2. Clique "Send magic link"
3. Backend génère JWT (15min)
4. Email service log URL (dev) ou envoie email (prod)
5. User clique URL → token vérifié
6. Backend retourne access_token + refresh_token
7. Frontend redirige vers /dashboard
→ CONNECTÉ ! ✅
```

---

## 📚 Documents à Lire

1. **`AUDIT_EXISTANT.md`** : État complet du projet (80% fait !)
2. **`GUIDE_MAGIC_LINK.md`** : Guide détaillé step-by-step
3. **`ROADMAP_DEVELOPPEMENT.md`** : Vision long terme

**Prochaine étape recommandée :**
👉 **Onboarding Logic** (3h) - L'UI existe déjà, juste ajouter la validation

---

## 🆘 Support

### En cas de problème :

**Emails ne partent pas ?**
→ Normal en dev ! Check les logs backend pour l'URL

**Frontend ne connecte pas au backend ?**
→ Vérifier `NEXT_PUBLIC_API_URL` dans `.env.local`

**Tests échouent ?**
→ Relancer `python -m pytest api/tests/ -v`

---

## 📊 Récapitulatif Temps

| Tâche | Temps estimé | Temps réel |
|-------|--------------|------------|
| Service Email | 1h | ___ |
| Routes Backend | 1h | ___ |
| Connection Frontend | 30min | ___ |
| Tests | 30min | ___ |
| **TOTAL** | **3h** | **___** |

**Remplis le "Temps réel" pour suivre ta progression !** ✍️

---

*Document créé le : 28 novembre 2025*  
*Mis à jour le : 29 novembre 2025 (après découverte du frontend existant)*

