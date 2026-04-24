__author__ = 'Suleiman Ali Mashuhuli'

from django.urls import path
from django.http import JsonResponse
from visitor.views.visits import VisitViewSet, check_in, check_out, resend_email
from visitor.views.hosts import HostViewSet, available
from visitor.views.audit import audit_list, retrieve_audit
from visitor.views.reports import summary, daily, export_csv, dashboard

def app_root(request):
    return JsonResponse({'message': 'Visitor API'})

urlpatterns = [
    path('', app_root),
    path('api/visits/', VisitViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/visits/<int:id>/check-in/', check_in, name='check_in'),
    path('api/visits/<int:id>/check-out/', check_out, name='check_out'),
    path('api/visits/<int:id>/resend-email/', resend_email, name='resend_email'),
    path('api/visits/active/', VisitViewSet.as_view({'get': 'active'}), name='visits-active'),
    path('api/hosts/', HostViewSet.as_view({'get': 'list'})),
    path('api/hosts/<int:id>/', HostViewSet.as_view({'get': 'retrieve'})),
    path('api/hosts/available/', available, name='available'),
    path('api/audit/', audit_list, name='audit_list'),
    path('api/audit/<int:id>/', retrieve_audit, name='retrieve_audit'),
    path('api/reports/summary/', summary, name='summary'),
    path('api/reports/daily/', daily, name='daily'),
    path('api/reports/export/csv/', export_csv, name='export_csv'),
    path('api/dashboard/', dashboard, name='dashboard'),
]