__author__ = 'Suleiman Ali Mashuhuli'

import csv
from io import BytesIO
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime
from rest_framework.decorators import api_view
from rest_framework import status
from ..models.visits import Visit
from rest_framework.response import Response
from django.http import StreamingHttpResponse
from ..serializers.visits import VisitSerializer
from django.db.models import Avg, F

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
                                check_out_at__isnull=True).count(),
        'check_out': summary_report.filter(status='check_out').count(),
        'still_inside': summary_report.filter(status='approved',
                                  checked_in_at__isnull=False,
                                  check_out_at__isnull=True).count(),
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
        for s in ['pending', 'approved', 'rejected', 'check_out']
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
        'Visitor', 'Type', 'ID Number', 'Contact',
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
                getattr(getattr(csvR.host, 'user', None), 'visitor_name', '') if csvR.host else '',
                csvR.status,
                csvR.created_at.isoformat() if csvR.created_at else '',
                csvR.approved_at.isoformat() if csvR.approved_at else '',
                csvR.checked_in_at.isoformat() if csvR.checked_in_at else '',
                csvR.check_out_at.isoformat() if csvR.check_out_at else '',
            ])

    response = StreamingHttpResponse(row_iter(), content_type='text/csv')
    filename = f'visitors_{date_from}_{date_to}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response


class _Echo:
    def write(self, x):
        return x


@api_view(['GET'])
def dashboard(request):
    today = timezone.localdate()
    today_start = timezone.make_aware(datetime.combine(today, datetime.min.time()))
    today_end = timezone.make_aware(datetime.combine(today, datetime.max.time()))
    now = timezone.now()

    pending_count = Visit.objects.filter(status='pending').count()

    approved_today = Visit.objects.filter(
        status='approved',
        approved_at__gte=today_start,
        approved_at__lte=today_end
    ).count()

    approved_last_30_days = Visit.objects.filter(
        status='approved',
        approved_at__isnull=False,
        approved_at__gte=now - timedelta(days=30)
    )
    if approved_last_30_days.exists():
        avg_secs = approved_last_30_days.annotate(
            approval_duration=F('approved_at') - F('created_at')
        ).aggregate(avg=Avg('approval_duration'))['avg']
        avg_approval_time = int(avg_secs.total_seconds()) if avg_secs else 0
    else:
        avg_approval_time = 0

    inside_count = Visit.objects.filter(
        status='approved',
        checked_in_at__isnull=False,
        check_out_at__isnull=True
    ).count()

    outside_count = Visit.objects.filter(
        check_out_at__isnull=False
    ).count()

    recent_visits = Visit.objects.select_related('host').order_by('-created_at')[:6]
    recent_visits_data = VisitSerializer(recent_visits, many=True).data

    return Response({
        'pending_count': pending_count,
        'approved_today': approved_today,
        'avg_approval_time': avg_approval_time,
        'inside_count': inside_count,
        'outside_count': outside_count,
        'recent_visits': recent_visits_data,
    })