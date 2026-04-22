__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from django.utils import timezone
from datetime import timedelta
from .enums.id_types import (ID_TYPES, STATUS_CHOICES, TYPE_VISIT)



class Visit(models.Model):
    """
        Visitor Model
    """

    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=30, default='')
    visitor_email = models.EmailField(max_length=15, default='')
    phoneNumber = models.CharField(max_length=10, default='')
    id_type = models.CharField(max_length=20, choices=ID_TYPES, default='national_id')
    id_number = models.CharField(max_length=10, unique=True, default='')
    visit_type = models.CharField(max_length=25, choices=TYPE_VISIT, default='external_walkin')
    organization = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending') 
    expected_duration_mins = models.PositiveIntegerField(help_text='Duration in minutes', default=30)
    purpose = models.TextField(max_length=500, default='')
    check_in_at = models.DateTimeField(null=True, blank=True)
    check_out_at = models.DateTimeField(null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    def check_in(self):
        if self.status == 'approved' and not self.approved_at:
            self.check_in_at = timezone.now()
        self.save()

    def check_out(self):
        if not self.check_out_at:
            self.check_out_at = timezone.now()
        self.save()

    class Meta:
        db_table = 'visit'