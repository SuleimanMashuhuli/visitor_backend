__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from django.utils import timezone
from datetime import timedelta

class Approval(models.Model):
    """
        Approval Model
    """

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'approval'