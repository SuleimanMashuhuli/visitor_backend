__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models

class Blacklist(models.Model):
    """
        Blacklist Model
    """

    name = models.CharField(max_length=100, default='')
    id_number = models.CharField(max_length=20, unique=True, default='')
    reason = models.TextField(max_length=500, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'blacklist'
