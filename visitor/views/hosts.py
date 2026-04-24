__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from ..models.host import Host
from ..serializers.host import HostSerializer


class HostViewSet(viewsets.ModelViewSet):
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


def available(request):
    hosts = Host.objects.filter(is_available=True)
    serializer = HostSerializer(hosts, many=True)
    return Response(serializer.data)