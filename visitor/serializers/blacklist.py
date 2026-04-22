__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from .models import (Blacklist)

class BlacklistSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = '__all__'
        read_only_fields = ['created_at']