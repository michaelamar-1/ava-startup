# 🗺️ ROADMAP DE DÉVELOPPEMENT - AvaFirst AI

**Date:** 28 Novembre 2025  
**État actuel:** Phase 2-4 complète ✅ | Tests stables ✅

---

## 📊 État Actuel du Projet

### ✅ Ce qui fonctionne déjà

#### Backend (FastAPI)
- ✅ Architecture Clean Architecture (DDD)
- ✅ Base de données PostgreSQL/SQLite avec SQLAlchemy
- ✅ Circuit breakers pour Vapi et Twilio (99.9% uptime)
- ✅ Rate limiting (DDoS protection)
- ✅ Observabilité (Prometheus metrics, correlation IDs)
- ✅ Tests : 35 passés, 14 skippés (documentés)
- ✅ Routes API pour :
  - `/api/v1/auth/*` - Login, signup, verify (partiellement implémenté)
  - `/api/v1/vapi/*` - Settings Vapi
  - `/api/v1/twilio-settings` - Configuration Twilio
  - `/api/v1/phone-numbers/*` - Gestion numéros
  - `/api/v1/webhooks/twilio/*` - Webhooks Twilio
  - `/api/v1/integrations/*` - Email/Calendar (stubs)

#### Frontend (Next.js 14)
- ✅ Architecture App Router Next.js 14
- ✅ UI avec Tailwind CSS + shadcn/ui
- ✅ Composants d'auth (SignInForm, ForgotPasswordForm)
- ✅ HTTP client unifié avec retry logic
- ✅ Logging structuré (JSON)

#### Infrastructure
- ✅ Docker compose
- ✅ Scripts de déploiement
- ✅ Monitoring Grafana/Prometheus ready
- ✅ CI/CD documentation

### ❌ Ce qui manque (Bloquants MVP)

#### 1. **Authentification Complète**
- ❌ Login avec numéro de téléphone (seulement email pour l'instant)
- ❌ Vérification SMS (Twilio Verify)
- ❌ Magic link email
- ❌ OAuth (Google/Microsoft) partiellement implémenté
- ❌ Session management robuste

#### 2. **Onboarding Flow**
- ❌ Wizard multi-étapes `/onboarding` (dossier vide)
- ❌ Sélection industrie + preset AVA
- ❌ Configuration téléphone (Vapi ou Twilio)
- ❌ Personnalisation voix et persona
- ❌ Test call en live

#### 3. **Dashboard Fonctionnel**
- ❌ Stats temps réel (appels, durée, coûts)
- ❌ Liste des appels avec filtres
- ❌ Lecture transcriptions
- ❌ Graphiques analytics

#### 4. **Gestion Numéros**
- ❌ Liste mes numéros (TODO dans `phone_numbers.py:382`)
- ❌ Achat numéro via Vapi
- ❌ Configuration routing par numéro

#### 5. **Intégrations Réelles**
- ❌ Email (stubs seulement)
- ❌ Calendar Google/Microsoft (stubs seulement)
- ❌ CRM (non implémenté)

---

## 🎯 ROADMAP - 3 Phases Prioritaires

### 🔥 PHASE 1 : MVP FONCTIONNEL (Priorité CRITIQUE)
**Objectif:** Application utilisable de bout en bout  
**Durée estimée:** 2-3 semaines  
**Impact:** Débloque les premiers utilisateurs

#### Semaine 1 : Authentification + Onboarding

##### 1.1 Authentification Email Complète (3 jours)
```
Tâches:
□ Backend: Finaliser /auth/login avec email + password
□ Backend: Implémenter magic link email
  - Route /auth/magic-link/send
  - Route /auth/magic-link/verify
  - Template email avec lien sécurisé (JWT token 15min)
□ Backend: Session management JWT robuste
  - Access token (1h)
  - Refresh token (7 jours)
  - Route /auth/refresh
□ Frontend: Page /login complète
  - Formulaire email + password
  - Option "Magic link" 
  - Messages d'erreur clairs
□ Frontend: Page /signup améliorée
  - Validation en temps réel
  - Confirmation email
□ Tests: E2E flow signup → login → session
```

**Livrable:** Utilisateur peut créer un compte et se connecter

##### 1.2 Onboarding Wizard (4 jours)
```
Tâches:
□ Frontend: Layout /onboarding avec stepper (5 étapes)

□ Étape 1: Bienvenue
  - Écran de bienvenue
  - Explication du processus
  - Bouton "Commencer"

□ Étape 2: Industrie
  - Sélection parmi 8-10 industries
  - Cards avec icônes
  - Backend: Route /onboarding/industries (liste)
  - Backend: Route /onboarding/preset/{industry} (config AVA par défaut)

□ Étape 3: Numéro de téléphone
  - Option A: Acheter via Vapi
    - Liste numéros disponibles
    - Sélection pays/ville
    - Backend: Route /phone-numbers/vapi/available
    - Backend: Route /phone-numbers/vapi/purchase
  - Option B: Importer Twilio
    - Formulaire Account SID + Auth Token
    - Vérification credentials
    - Import numéros existants
    - Backend: Route /phone-numbers/twilio/verify
    - Backend: Route /phone-numbers/twilio/import

□ Étape 4: Personnalisation AVA
  - Choix voix (11labs, Azure)
  - Langue (FR, EN, ES, etc.)
  - Ton (professionnel, amical, enjoué)
  - Message d'accueil personnalisé
  - Backend: Route /ava-profiles (POST)

□ Étape 5: Test & Finalisation
  - Bouton "Appeler pour tester"
  - Affichage transcript en temps réel
  - Validation et redirection /dashboard
  - Backend: Route /onboarding/complete

□ Tests: E2E flow onboarding complet
```

**Livrable:** Nouvel utilisateur peut setup son AVA en < 10min

#### Semaine 2 : Dashboard Fonctionnel

##### 2.1 Dashboard Core (3 jours)
```
Tâches:
□ Backend: Route /calls (liste avec pagination)
  - Filtres: date, status, duration
  - Tri: date desc par défaut
  - Pagination: 20 par page

□ Backend: Route /calls/{id} (détail)
  - Transcript complet
  - Recording audio
  - Métadonnées

□ Backend: Route /analytics/summary
  - Nombre total appels (today, week, month)
  - Durée moyenne
  - Coût total
  - Top 5 topics

□ Frontend: Page /dashboard
  - Cards stats (4 KPIs principaux)
  - Graphique appels par jour (7 derniers jours)
  - Liste 10 derniers appels
  - Bouton "Voir tous les appels"

□ Frontend: Page /calls
  - Tableau avec filtres
  - Pagination
  - Click → modal détail

□ Frontend: Composant CallDetail
  - Player audio
  - Transcript scrollable
  - Boutons actions (delete, export)

□ Tests: E2E navigation dashboard → calls
```

**Livrable:** Utilisateur peut voir ses appels et analytics

##### 2.2 Gestion Numéros (2 jours)
```
Tâches:
□ Backend: Implémenter /phone-numbers/my-numbers (TODO ligne 382)
  - Query DB pour numéros de l'user
  - Format: [{id, number, provider, status, created_at}]

□ Backend: Route /phone-numbers/{id}/configure
  - Heures d'ouverture
  - Routing (assistant ID)
  - Forwarding number

□ Frontend: Page /phone-numbers
  - Liste mes numéros
  - Bouton "Ajouter numéro"
  - Modal configuration par numéro

□ Tests: CRUD numéros
```

**Livrable:** Utilisateur peut gérer ses numéros

#### Semaine 3 : Polish + Testing

##### 3.1 UX Polish (2 jours)
```
Tâches:
□ Loading states partout
□ Error handling graceful
□ Messages toast notifications
□ Animations transitions
□ Responsive mobile complet
□ Dark mode (optionnel)
```

##### 3.2 Tests E2E (2 jours)
```
Tâches:
□ Setup Playwright
□ Test E2E: Signup → Onboarding → Dashboard
□ Test E2E: Login → Voir appels → Logout
□ Test E2E: Ajouter numéro → Configurer → Tester
□ CI/CD: Intégrer tests E2E
```

##### 3.3 Documentation Utilisateur (1 jour)
```
Tâches:
□ Guide de démarrage rapide
□ FAQ
□ Troubleshooting commun
□ Vidéo demo 2min
```

**Livrable MVP:** Application complète utilisable par premiers clients

---

### 🚀 PHASE 2 : INTÉGRATIONS & SCALING (Post-MVP)
**Durée estimée:** 2-3 semaines

#### 2.1 Intégrations Email/Calendar Réelles
```
Tâches:
□ Email: Remplacer stubs par Resend/SendGrid
  - Templates transactionnels
  - Résumés d'appels
  - Notifications

□ Calendar Google: OAuth flow complet
  - Consent screen
  - Tokens refresh
  - Sync événements
  - Création RDV depuis appel

□ Calendar Microsoft: Même flow

□ Tests: Intégrations E2E
```

#### 2.2 Features Avancées
```
Tâches:
□ Multi-utilisateurs par organisation
  - Rôles (admin, user, viewer)
  - Permissions granulaires

□ Billing & Plans
  - Stripe integration
  - Plans Free/Pro/Enterprise
  - Usage tracking

□ CRM Integration
  - Hubspot connector
  - Salesforce connector
  - Pipedrive connector

□ Webhooks
  - Permettre clients de recevoir events
  - Documentation API

□ White-labeling
  - Custom branding
  - Custom domain
```

#### 2.3 Performance & Scale
```
Tâches:
□ Caching Redis
  - Session cache
  - API responses cache
  - Rate limit storage

□ CDN pour assets
□ Database indexing optimization
□ Horizontal scaling prep
  - Stateless backend
  - Load balancer ready
```

---

### 🌟 PHASE 3 : ADVANCED FEATURES (Futur)
**Durée estimée:** 1-2 mois

#### 3.1 AI/ML Features
```
Tâches:
□ Sentiment analysis des appels
□ Auto-categorization
□ Predictive analytics
□ Recommendations automatiques
```

#### 3.2 Mobile Apps
```
Tâches:
□ React Native app
  - iOS
  - Android
□ Push notifications
□ Appels en app
```

#### 3.3 Enterprise Features
```
Tâches:
□ SSO (SAML, OKTA)
□ Audit logs complets
□ Compliance (GDPR, HIPAA)
□ SLA monitoring
□ Dedicated instances
```

---

## 📋 PLAN D'ACTION IMMÉDIAT (Cette Semaine)

### Jour 1-2 : Authentication Email + Magic Link

**Backend:**
```bash
# 1. Créer le service d'email
touch api/src/infrastructure/email/email_service.py

# 2. Implémenter magic link
# Fichier: api/src/presentation/api/v1/routes/auth.py
# - Route POST /auth/magic-link/send
# - Route GET /auth/magic-link/verify?token=xxx

# 3. Améliorer JWT tokens
# Fichier: api/src/core/security.py
# - create_access_token (1h expiry)
# - create_refresh_token (7 days expiry)
# - verify_token avec rotation

# 4. Tests
touch api/tests/test_auth_magic_link.py
```

**Frontend:**
```bash
# 1. Améliorer page login
# Fichier: webapp/app/(public)/[locale]/(auth)/login/page.tsx
# - Ajouter option "Magic Link"
# - Formulaire avec validation
# - Loading states

# 2. Créer page verify magic link
touch webapp/app/(public)/[locale]/(auth)/verify/page.tsx

# 3. Server actions
touch webapp/app/(public)/[locale]/(auth)/actions.ts
```

### Jour 3-5 : Onboarding Wizard Foundation

**Backend:**
```bash
# 1. Routes onboarding
touch api/src/presentation/api/v1/routes/onboarding.py
# - GET /onboarding/industries
# - GET /onboarding/preset/{industry}
# - POST /onboarding/complete

# 2. Service onboarding
touch api/src/application/services/onboarding_service.py
```

**Frontend:**
```bash
# 1. Layout onboarding
mkdir -p webapp/app/(app)/[locale]/onboarding
touch webapp/app/(app)/[locale]/onboarding/layout.tsx
touch webapp/app/(app)/[locale]/onboarding/page.tsx

# 2. Composant Stepper
touch webapp/components/onboarding/stepper.tsx

# 3. Steps components
touch webapp/components/onboarding/step-welcome.tsx
touch webapp/components/onboarding/step-industry.tsx
touch webapp/components/onboarding/step-phone.tsx
touch webapp/components/onboarding/step-customize.tsx
touch webapp/components/onboarding/step-test.tsx
```

---

## 🎯 Métriques de Succès

### Phase 1 (MVP)
- [ ] Temps signup → premier appel < 10 minutes
- [ ] Taux de complétion onboarding > 80%
- [ ] 0 bugs bloquants
- [ ] Tests E2E 100% passés
- [ ] Load time pages < 2s

### Phase 2 (Scale)
- [ ] Support 100+ users concurrents
- [ ] API response time p95 < 500ms
- [ ] Uptime > 99.5%
- [ ] 3+ intégrations actives

### Phase 3 (Advanced)
- [ ] Support 1000+ users
- [ ] Mobile apps rated > 4.5/5
- [ ] Enterprise clients > 5

---

## 🛠️ Quick Start - Commencer Maintenant

### Option 1 : Authentification (Recommandé)
```bash
# 1. Créer branche
git checkout -b feature/auth-magic-link

# 2. Backend: Implémenter magic link
cd api
source .venv/bin/activate

# Éditer:
# - api/src/presentation/api/v1/routes/auth.py (ajouter routes)
# - api/src/infrastructure/email/email_service.py (créer)
# - api/tests/test_auth_magic_link.py (tests)

# 3. Tester
python -m pytest api/tests/test_auth_magic_link.py -v

# 4. Frontend: UI magic link
cd ../webapp
# Éditer:
# - app/(public)/[locale]/(auth)/login/page.tsx

npm run dev
```

### Option 2 : Onboarding Wizard
```bash
# 1. Créer branche
git checkout -b feature/onboarding-wizard

# 2. Backend: Routes onboarding
cd api
# Créer api/src/presentation/api/v1/routes/onboarding.py

# 3. Frontend: Structure onboarding
cd ../webapp
mkdir -p app/(app)/[locale]/onboarding
mkdir -p components/onboarding

# 4. Implémenter step by step
```

### Option 3 : Dashboard Stats
```bash
# 1. Créer branche
git checkout -b feature/dashboard-stats

# 2. Backend: Analytics routes
cd api
# Créer api/src/presentation/api/v1/routes/analytics.py

# 3. Frontend: Dashboard composants
cd ../webapp
# Améliorer app/(app)/[locale]/dashboard/page.tsx
```

---

## 📚 Resources Utiles

### Documentation à lire
- [ ] `IMPLEMENTATION_PLAN.md` - Plan détaillé complet
- [ ] `api/tests/CORRECTIONS_TESTS.md` - Guide des tests
- [ ] `README.md` - Vue d'ensemble

### Fichiers clés à comprendre
```
Backend:
- api/src/presentation/api/v1/routes/auth.py (authentification)
- api/src/infrastructure/external/vapi_client.py (client Vapi)
- api/src/application/services/twilio.py (client Twilio)
- api/tests/conftest.py (fixtures tests)

Frontend:
- webapp/lib/api/client.ts (HTTP client)
- webapp/app/(app)/[locale]/dashboard/page.tsx (dashboard)
- webapp/components/auth/sign-in-form.tsx (login UI)
```

### Commandes fréquentes
```bash
# Lancer app complète
./scripts/dev.sh

# Backend seul
cd api && source .venv/bin/activate && uvicorn api.main:app --reload

# Frontend seul
cd webapp && npm run dev

# Tests backend
cd api && python -m pytest api/tests/ -v

# Tests un fichier
python -m pytest api/tests/test_auth.py -v

# Linter
cd api && ruff check .
cd webapp && npm run lint
```

---

## ❓ Questions Fréquentes

### Q: Par où commencer ?
**R:** Commence par l'authentification (Option 1). C'est la fondation de tout le reste.

### Q: Combien de temps pour le MVP ?
**R:** 2-3 semaines à temps plein, 4-6 semaines à mi-temps.

### Q: Puis-je skip l'onboarding ?
**R:** Non, c'est critique pour l'expérience utilisateur. Sans onboarding, les users sont perdus.

### Q: Les tests sont-ils obligatoires ?
**R:** Oui pour les features core (auth, onboarding, calls). Optionnel pour les pages simples.

### Q: Database migrations ?
**R:** Utilise Alembic pour le backend :
```bash
cd api
alembic revision --autogenerate -m "Add magic_link_token to users"
alembic upgrade head
```

---

## 🎉 Conclusion

**Tu as maintenant :**
- ✅ Une vision claire de l'état actuel
- ✅ Un plan d'action structuré en 3 phases
- ✅ Des tâches concrètes pour commencer
- ✅ Les ressources nécessaires

**Prochaine étape recommandée :**  
👉 **Commencer par l'authentification magic link** (le plus impactant pour l'expérience utilisateur)

**Besoin d'aide ?**  
- Relis `IMPLEMENTATION_PLAN.md` pour plus de détails
- Les tests dans `api/tests/` montrent des exemples d'utilisation
- Tous les fixtures sont documentés dans `api/tests/conftest.py`

---

**Bonne chance ! 🚀**

*Document créé le : 28 novembre 2025*

