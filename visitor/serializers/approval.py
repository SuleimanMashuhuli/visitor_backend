__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from ..models.approval import Approval

class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = '__all__'
        read_only_fields = ['expires_at','created_at']
