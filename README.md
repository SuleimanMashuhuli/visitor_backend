
# Visitor Backend Architecture

Django Backend for a visitor management system with tokenized email links, scheduled tasks and async email processing.

## Configuration

### Environment Variables
```bash
# Database
DATABASE_URL=postgres://user:pass@localhost:5432/visitors

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_BACKEND=sgbackend.SendGridBackend
SENDGRID_API_KEY=SG.xxxxxx

---

## Directory Structure
```
visitor_backend/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── celery.py
├── apps/
│   ├── users/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── permissions.py
│   ├── visit/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── tasks.py
│   │   └── signals.py
│   ├── blacklist/
│   └── auditlog/
├── templates/
│   └── email/
│       └── visit_request.html
├── conftest.py
└── manage.py
```
