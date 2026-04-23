__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import (viewsets, status)
from rest_framework.decorators import action 
from rest_framework.response import Response
from .models.host import (Host)
from .serializers.host import (HostSerializer)
from django.permissions import (IsAuthenticated, IsAdminUser)

class HostSerializer(viewsets.ModelViewSet):
    """
        GET	/api/action/{token}/	One-click approve/reject from email
        list	GET /api/hosts/	Dropdown source for booking form
        destroy	GET /api/hosts/{id}/	
        create / update / destroy	Standard	Admin only
        @action available	GET /api/hosts/available/	Filter is_available=True
    """
    queryset = Host.objects.all()
    serializer_class = HostSerializer

   def get_permissions(self):
        if self.action in ('list', 'retrieve', 'available'):
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def available(self, request):
        hosts = self.get_queryset().filter(is_available=True)
        serializer = self.get_serializer(hosts, many=True)
        return Response(serializer.data)


