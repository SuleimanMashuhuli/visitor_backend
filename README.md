# Visitor Management Backend

Django REST API backend for managing visitor check-ins, host approvals, and visit tracking.

## Features

- Visitor registration and check-in/check-out tracking
- Host approval workflow with tokenized email links
- Blacklist management for banned visitors
- Audit logging for compliance
- Scheduled visit expiration


## Project Structure

```
visitor_backend/
├── visitor/
│   ├── models/
│   │   ├── visit.py        # Visit model
│   │   ├── host.py         # Host model
│   │   ├── profiles.py     # Visitor profiles
│   │   ├── auditlog.py     # Audit logging
│   │   └── approval.py    # Approval workflow
│   ├── serializers/       # DRF serializers
│   ├── views/             # API views
│   ├── services/          # Business logic
│   ├── enums/             # Constants
│   └── urls.py            # URL routing
├── visitor_backend/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URLs
│   └── wsgi.py            # WSGI config
├── manage.py
└── requirements.txt
```

## Models

- **Visit**: Tracks visitor check-in/check-out, status, and duration
- **Host**: Employee who receives visitors
- **Profiles**: Visitor information and history
- **Blacklist**: Banned visitors
- **AuditLog**: Compliance audit trail
- **Approval**: Visit approval workflow