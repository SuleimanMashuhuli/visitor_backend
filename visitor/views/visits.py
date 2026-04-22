__author__ = 'Suleiman Ali Mashuhuli'

"""
    list	GET /api/visits/	Paginated, filterable (?status=&type=&host=&q=)
    retrieve	GET /api/visits/{id}/	Single visit + audit trail
    create	POST /api/visits/	Book visit → checks blacklist → triggers Celery email
    update / partial_update	PUT/PATCH /api/visits/{id}/	Edit before approval
    destroy	DELETE /api/visits/{id}/	Admin only
    @action check_in	POST /api/visits/{id}/check-in/	Security marks arrival
    @action check_out	POST /api/visits/{id}/check-out/	Security marks exit
    @action resend_email	POST /api/visits/{id}/resend-email/	Re-queue host notification
    @action by_code	GET /api/visits/by-code/{code}/	Lookup by 8-char pass
    @action active	GET /api/visits/active/	Currently inside
"""


from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime, date
from .models import (Profiles, Host, Visit, Blacklist, AuditLog, Approval)
from .serializers import (ProfilesSerializer, HostSerializer, VisitSerializer, BlacklistSerailizer, AuditLogSerializer, ApprovalSerializer)
from django.http import (JsonResponse, HttpResponse)



def book_visit(request):
    """
        Contains Book a Visit Enpoint
    """

def blacklist(request):
    """
        Contains Blacklist Entry
    """