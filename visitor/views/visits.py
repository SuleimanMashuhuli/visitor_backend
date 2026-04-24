__author__ = 'Suleiman Ali Mashuhuli'

from django.utils import timezone
from datetime import (timedelta, datetime, date)
from rest_framework import (viewsets, status)
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.visits import Visit
from ..serializers.visits import VisitSerializer

class VisitViewSet(viewsets.ModelViewSet):
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        visit = self.get_object()
        visit.check_in()
        return Response(self.get_serializer(visit).data)
    
    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        visit = self.get_object()
        visit.check_out()
        return Response(self.get_serializer(visit).data)
    
    @action(detail=True, methods=['post'])
    def resend_email(self, request, pk):
        visit = self.get_object()
        from visitor.tasks.tasks import send_host_approval_email
        send_host_approval_email.delay(visit.id)
        return Response({'message': "Email sent"})


def check_in(request, id):
    from rest_framework.response import Response
    from rest_framework import status
    try:
        visit = Visit.objects.get(id=id)
        visit.check_in()
        return Response(VisitSerializer(visit).data, status=status.HTTP_200_OK)
    except Visit.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


def check_out(request, id):
    from rest_framework.response import Response
    from rest_framework import status
    try:
        visit = Visit.objects.get(id=id)
        visit.check_out()
        return Response(VisitSerializer(visit).data, status=status.HTTP_200_OK)
    except Visit.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


def resend_email(request, id):
    from rest_framework.response import Response
    from rest_framework import status
    from visitor.tasks.tasks import send_host_approval_email
    try:
        visit = Visit.objects.get(id=id)
        send_host_approval_email.delay(visit.id)
        return Response({'message': "Email sent"}, status=status.HTTP_200_OK)
    except Visit.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
