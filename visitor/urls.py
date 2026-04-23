__author__ = 'Suleiman Ali Mashuhuli'

from django.urls import path
from . import views

urlpatterns = [
    path('', app_root),
    # Visit
    path('/api/visits/', ),
    path('/api/visits/{id}/check-in/', ), # Security marks arrival
    path('/api/visits/{id}/check-out/', ), # Security marks exit
    path('/api/visits/{id}/resend-email/', ) # Re-queue host notification
    path('/api/visits/active/', ), # Currently inside
    # Host
    path('/api/action/{token}/, ') # One-click approve/reject email
    path('/api/hosts/', ) # List
    path('/api/hosts/{id}/') # Retrieve
    path('/api/hosts/available/', ),
    # AuditLog
    path('/api/audit/', ), # List
    path('/api/audit/{id}/', ), # Retrieve
    # ReportsView
    path('/api/reports/summary/?date=', ),
    path('/api/reports/daily/?date=', )
    path('/api/reports/export/csv/?from=&to=', ),
]