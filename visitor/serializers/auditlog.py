__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from .models.auditlog import (AuditLog)

class AuditLogSerializer(serializers.ModelSerializer):
    class Meat:
        model = AuditLog
        fields = '__all__'
        read_only_fields = ['created_at']