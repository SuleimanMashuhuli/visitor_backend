__author__ = 'Suleiman Ali Mashuhuli'

from django.shortcuts import render
from django.utils import timezone
from datetime import (timedelta, date, datetime)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import status
from .serializers.auditlog import (AuditLogSerializer)
from .models.auditlog import (AuditLog)


@api_view(['GET'])
def _parse_date(value):
    if not value:
        return None
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return "INVALID"


@api_view(['GET'])
def audit_list(request):
    ad_list = AuditLog.objects.select_related('actor', 'visit').all()

    actor = request.query_params.get('actor')
    action_param = request.query_params.get('action')
    visit = request.query_params.get('visit')
    date_from = _parse_date(request.query_params.get('date_from'))
    date_to = _parse_date(request.query_params.get('date_to'))

    if date_from == "INVALID" or date_to == "INVALID":
        return Response({"detail": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    if actor:
        ad_list = ad_list.filter(actor_id=actor)
    if action_param:
        ad_list = ad_list.filter(action__iexact=action_param)
    if visit:
        ad_list = ad_list.filter(visit_id=visit)
    if date_from:
        ad_list = ad_list.filter(created_at__date__gte=date_from)
    if date_to:
        ad_list = ad_list.filter(created_at__date__lte=date_to)

    ad_list = ad_list.order_by('-created_at')
    return Response(AuditLogSerializer(ad_list, many=True).data)


@api_view(['GET'])
def retrieve_audit(request, id):
    try:
        entry = AuditLog.objects.select_related('actor', 'visit').get(id=id)
    except AuditLog.DoesNotExist:
        return Response({"detail": "Audit log not found."}, status=status.HTTP_404_NOT_FOUND)
    return Response(AuditLogSerializer(entry).data)