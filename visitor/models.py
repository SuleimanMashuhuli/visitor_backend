__author__ = 'Suleiman Ali Mashuhuli'

from django.db import models
from django.utils import timezone
from .enums.id_types import (ID_TYPES, STATUS_CHOICES, TYPE_VISIT, ROLES_CHOICE)



class Profiles(models.Model):
    """
        Profiles Model
    """
    username = models.CharField(max_length=10, default='')
    email = models.EmailField(max_length=20, default='')
    password = models.CharField(max_length=15, default='')
    role = models.CharField(max_length=10, default='')   # ========IMPORT ROLES========
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'profile_table'

class Visit(models.Model):
    """
        Visitor Model
    """
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    visitor_name = models.CharField(max_length=30, default='')
    visitor_email = models.EmailField(max_length=15, default='')
    phoneNumber = models.CharField(max_length=10, default='')
    id_type = models.CharField(max_length=20, default='')   # ========IMPORT ID TYPE========
    id_number = models.CharField(max_length=10, unique=True, default='')
    visit_type = models.CharField(max_length=25, default='') # ========IMPORT VISIT TYPE========
    organization = models.CharField(max_length=100, default='')
    status = models.CharField(max_length=10, default='')    # ========IMPORT STATUS========
    expected_duration_mins = models.PositiveIntegerField(help_text='Duration in minutes', default=30)
    purpose = models.TextField(max_length=50, default='')
    check_in_at = models.DateField(null=True, blank=True)
    check_out_at = models.DateField(null=True, blank=True)
    approved_at = models.DateField(null=True, blank=True)
    expires_at = models.DateField()  # ========CREATED AT + 24 HRS========
    created_at = models.DateField(auto_add_now=True)

    class Meta:
        db_table = 'visit_table'


class Host(models.Model):
    """
        Visit Model
    """
    host_name = models.CharField(max_length=100, default='')
    host_email = models.EmailField(max_length=15, default='')
    department = models.CharField(max_length=10, default='')
    created_at = models.DateField(auto_add_now=True)

    class Meta:
        db_table = 'host_table'


class Blacklist(models.Model):
    """
        Blacklist Model
    """
    name = models.CharField(max_length=100, default='')
    id_number = models.CharField(max_length=10, unique=True, default='')
    reason = models.TextField(max_length=200, default='')
    is_active = models.BooleanField(default=True)
    created_at = models.DateField(auto_add_now=True)

    class Meta:
        db_table = 'blacklist_table'


class AuditLog(models.Model):
    """
        AuditLog Model
    """
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    action = models.CharField(default='')  #========STATUS CHOICE======
    detail = models.TextField(max_length=200, default='')
    created_at = models.DateField(auto_add_now=True)

    class Meta:
        db_table = 'audit_table'

class Approval(models.Model):
    """
        Approval Model
    """
    visit = models.ForeignKey(Visit, on_delete=models.CASCADE)
    expires_at = models.DateField(default='')      # ========CREATED AT + 24 HRS========
    created_at = models.DateField(auto_add_now=True)

    class Meta:
        db_table = 'approval_table'