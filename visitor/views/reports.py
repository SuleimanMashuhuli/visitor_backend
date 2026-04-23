__author__ = 'Suleiman Ali Mashuhuli'

import csv
from io import BytesIO
from django.shortcuts import render
from django.utils import timezone
from datetime import (timedelta, date, datetime)
from rest_framework.decorators import api_view
from rest_framework import status
from .models.visits import (Visit)
from rest_framework.response import Response
from django.http import (HttpResponse, JsonResponse)

def _parse_date(value):
    """Parse YYYY-MM-DD or return today."""
    if not value:
        return timezone.localdate()
    try:
        return datetime.strptime(value, "%Y-%m-%d").date()
    except ValueError:
        return None

@api_view(['GET'])
def summary(request):
    """
        GET /api/reports/summary/?date=YYYY-MM-DD
        KPI tiles for dashboard.
    """
    date_selection = _parse_date(request.query_params.get('date'))
    if date_selection is None:
        return Response(
            {'detail': 'Invalid date format. Use YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    summary_report = Visit.objects.filter(created_at__date=date_selection)

    data = {
        'date': date_selection,
        'total': summary_report.count(),
        'pending': summary_report.filter(status='pending').count(),
        'approved': summary_report.filter(status='approved').count(),
        'rejected': summary_report.filter(status='rejected').count(),
        'checked_in': summary_report.filter(checked_in_at__isnull=False,
                                checked_out_at__isnull=True).count(),
        'checked_out': summary_report.filter(status='checked_out').count(),
        'still_inside': summary_report.filter(status='approved',
                                  checked_in_at__isnull=False,
                                  checked_out_at__isnull=True).count(),
    }
    return Response(data)

@api_view(['GET'])
def daily(request):
    """
        GET /api/reports/daily/?date=YYYY-MM-DD
        Breakdown by visitor_type and status.
    """
    selected_date = _parse_date(request.query_params.get('date'))
    if selected_date is None:
        return Response(
            {'detail': 'Invalid date format. Use YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    daily_report = Visit.objects.filter(created_at__date=selected_date)
    total = daily_report.count()

    by_type = [
        {
            'type': t,
            'count': daily_report.filter(visitor_type=t).count(),
        }
        for t in ['internal', 'external_appointment', 'external_walkin']
    ]
    by_status = [
        {
            'status': s,
            'count': daily_report.filter(status=s).count(),
        }
        for s in ['pending', 'approved', 'rejected', 'checked_out']
    ]

    return Response({
        'date': selected_date,
        'total': total,
        'by_type': by_type,
        'by_status': by_status,
    })

@api_view(['GET'])
def export_csv(request):
    """
        GET /api/reports/export/csv/?from=YYYY-MM-DD&to=YYYY-MM-DD
        Streams a CSV of visits in the date range.
    """
    date_from = _parse_date(request.query_params.get('from'))
    date_to = _parse_date(request.query_params.get('to'))

    if date_from is None or date_to is None:
        return Response(
            {'detail': 'Invalid date(s). Use YYYY-MM-DD.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    csv_report = (Visit.objects
          .select_related('host__user')
          .filter(created_at__date__gte=date_from,
                  created_at__date__lte=date_to)
          .order_by('-created_at'))

    header = [
        'Code', 'Visitor', 'Type', 'ID Number', 'Contact',
        'Organization', 'Host', 'Status',
        'Booked At', 'Approved At', 'Checked In', 'Checked Out',
    ]

    def row_iter():
        writer = csv.writer(_Echo())
        yield writer.writerow(header)
        for csvR in csv_report.iterator():
            yield writer.writerow([
                csvR.code,
                csvR.visitor_name,
                csvR.visitor_type,
                csvR.id_number,
                csvR.contact,
                csvR.organization or '',
                getattr(getattr(csvR.host, 'user', None), 'full_name', '') if csvR.host else '',
                csvR.status,
                csvR.created_at.isoformat() if csvR.created_at else '',
                csvR.approved_at.isoformat() if csvR.approved_at else '',
                csvR.checked_in_at.isoformat() if csvR.checked_in_at else '',
                csvR.checked_out_at.isoformat() if csvR.checked_out_at else '',
            ])

    response = StreamingHttpResponse(row_iter(), content_type='text/csv')
    filename = f'visitors_{date_from}_{date_to}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response