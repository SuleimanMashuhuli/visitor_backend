__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from ..enums.id_types import ROLES_CHOICE

class Profiles(models.Model):
    """
        Profiles Model
    """

    username = models.CharField(max_length=15, default='')
    email = models.EmailField(max_length=20, default='')
    password = models.CharField(max_length=15, default='')
    role = models.CharField(max_length=10, choices=ROLES_CHOICE, default='security') 
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile'