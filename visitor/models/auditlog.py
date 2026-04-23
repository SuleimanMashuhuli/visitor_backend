__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from .enums.id_types import (STATUS_CHOICES)

class AuditLog(models.Model):
    """
        AuditLog Model
    """

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    actor = models.ForeignKey('role.Profiles', on_delete=models.CASCADE, related_name='audit_logs')
    action = models.CharField(choices=STATUS_CHOICES, default='')
    detail = models.TextField(max_length=200, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'audit'