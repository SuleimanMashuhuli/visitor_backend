__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models

class Host(models.Model):
    """
        Visit Model
    """

    host_name = models.CharField(max_length=100, default='')
    host_email = models.EmailField(max_length=15, default='')
    department = models.CharField(max_length=50, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'host'