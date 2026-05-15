__author__ = 'Suleiman Ali Mashuhuli'


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.visits import Visit
from ..serializers.visits import VisitSerializer
from visitor.tasks.tasks import send_host_approval_email


class VisitViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing visits with check-in/check-out functionality.
    """
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
    
    @action(detail=True, methods=['post'])
    def check_in(self, request, pk=None):
        """
        Check in a visit.
        """
        visit = self.get_object()
        if visit.checked_in_at:
            return Response(
                {'detail': 'Visit already checked in'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        visit.check_in()
        return Response(
            self.get_serializer(visit).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def check_out(self, request, pk=None):
        """
        Check out a visit.
        """
        visit = self.get_object()
        
        if not visit.checked_in_at:
            return Response(
                {'detail': 'Visit not checked in yet'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        visit.check_out()
        return Response(
            self.get_serializer(visit).data,
            status=status.HTTP_200_OK
        )
    
    @action(detail=True, methods=['post'])
    def resend_email(self, request, pk=None):
        """
        Resend host approval email for a visit.
        """
        visit = self.get_object()
        send_host_approval_email.delay(visit.id)
        return Response(
            {'message': "Email sent successfully"},
            status=status.HTTP_200_OK
        )