__author__ = 'Suleiman Ali Mashuhuli'

from rest_framework import serializers
from ..models.profiles import Profiles

class ProfilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profiles
        fields = '__all__'
        read_only_fields = []