__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from ..models.host import Host

class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Host
        fields = '__all__'
        read_only_fields = ['created_at']