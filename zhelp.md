### 🔴 Issues / Corrections Needed

**3. Incomplete Features**
- `services/` directory is empty - no business logic layer
- No email templates
- No approval token generation on Visit model
- No authentication (JWT/Token) setup
**4. Data Model Issues**
- Missing `user` relationship in Host model
- No indexes on frequently queried fields
**5. Configuration Gaps**
- No `.env` file setup
- DEBUG=True in production settings
- Redis/Celery configs lack error handling
- No migrations generated
---



1. AuthViewSet (or use djoser defaults)
Method	Endpoint	Purpose
POST register	/api/auth/register/	Create user (receptionist/host)
POST login	/api/auth/login/	Email + password → JWT
POST logout	/api/auth/logout/	Blacklist refresh token
POST refresh	/api/auth/refresh/	Rotate JWT
GET me	/api/auth/me/	Current user profile
POST google	/api/auth/google/	Google OAuth callback
POST password_reset	/api/auth/password/reset/	Request reset email
POST password_reset_confirm	/api/auth/password/reset/confirm/	Apply new password


8. DashboardView (APIView)
Method	Endpoint	Purpose
GET	/api/dashboard/ --- Single call returning: pending count, approved today, avg approval time, inside vs out, recent 6 visits