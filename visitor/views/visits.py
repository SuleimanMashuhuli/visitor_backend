__author__ = 'Suleiman Ali Mashuhuli'

from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime, date
from rest_framework import viewsets
from rest_framework import action
from rest_framework import status
from rest_framework.response import Response
from .models import (Visit)
from .serializers import (VisitSerializer)
from django.http import (JsonResponse, HttpResponse)


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
        send_email_notification.delay(visit.id)
        return Response({'message': "Email sent"})
