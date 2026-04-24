__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from ..models.visits import Visit

class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = '__all__'
        read_only_fields = ['expires_at', 'created_at']
        filterset_fields = ['status', 'visitor_type', 'host']
        search_fields = ['visitor_name', 'host']