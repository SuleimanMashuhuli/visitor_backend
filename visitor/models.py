__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from django.utils import timezone
from datetime import timedelta
from .enums.id_types import (ID_TYPES, STATUS_CHOICES, TYPE_VISIT, ROLES_CHOICE)


class Profiles(models.Model):
    """
        Profiles Model
    """

    username = models.CharField(max_length=10, default='')
    email = models.EmailField(max_length=20, default='')
    password = models.CharField(max_length=15, default='')
    role = models.CharField(max_length=10, choices=ROLES_CHOICE, default='security') 
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile_table'

class Host(models.Model):
    """
        Visit Model
    """

    host_name = models.CharField(max_length=100, default='')
    host_email = models.EmailField(max_length=15, default='')
    department = models.CharField(max_length=10, default='')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'host_table'


class Visit(models.Model):
    """
        Visitor Model
    """

    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=30, default='')
    visitor_email = models.EmailField(max_length=15, default='')
    phoneNumber = models.CharField(max_length=10, default='')
    id_type = models.CharField(max_length=20, choices=ID_TYPES default='national_id')
    id_number = models.CharField(max_length=10, unique=True, default='')
    visit_type = models.CharField(max_length=25, choices=TYPE_VISIT, default='external_walkin')
    organization = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='') 
    expected_duration_mins = models.PositiveIntegerField(help_text='Duration in minutes', default=30)
    purpose = models.TextField(max_length=500, default='')
    check_in_at = models.DateField(null=True, blank=True)
    check_out_at = models.DateField(null=True, blank=True)
    approved_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'visit_table'


class Blacklist(models.Model):
    """
        Blacklist Model
    """

    name = models.CharField(max_length=100, default='')
    id_number = models.CharField(max_length=20, unique=True, default='')
    reason = models.TextField(max_length=500, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'blacklist_table'


class AuditLog(models.Model):
    """
        AuditLog Model
    """

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    action = models.CharField(choices=STATUS_CHOICES, default='')
    detail = models.TextField(max_length=200, default='')
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        db_table = 'audit_table'

class Approval(models.Model):
    """
        Approval Model
    """

    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    expires_at = models.DateField(default='')
    created_at = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'approval_table'