
# CRITICAL (will crash or not work):
1. Fix visitor/tasks/tasks.py — visit.approval_token doesn't exist;
3. Run makemigrations and migrate — Approval model has no migration yet
5. Add REST_FRAMEWORK config in settings.py

# NEEDS IMPLEMENTATION:
10. visitor/views/auth.py — complete stub, entire auth system missing (register, login, JWT, etc.)
11. visitor/services/ — empty, no business logic layer
12. visitor/admin.py — empty, register your models
13. visitor/tests.py — no tests

# NICE TO HAVE:
14. Docker Compose files — all incomplete/empty
15. Empty __init__.py files littered everywhere (minor cleanup)
16. Profiles model stores passwords in plain text — should use Django's AbstractUser