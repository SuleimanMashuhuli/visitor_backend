from celery import shared_task
from .models.visits import (Visit)
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

@shared_task
def send_host_approval_email(self, id):
    visit = Visit.objects.select_related('host').get(id=id)
    approve_url = f"https://yourapp.com/api/action/{visit.approval_token}?decision=approve"
    reject_url = f"https://yourapp.com/api/action/{visit.approval_token}?decision=reject"

    send_mail(
        subject = f"Visitor request: {visit.visitor_name}
        message= f"Approve: {approve_url}\nReject: {reject_url}",
        from_email= "noreply@suleimandev.com",
        recipient_list=[visit.host.email],
    )

@shared_task
def expire_pending_visits():
    cutoff = timezone.now() - timedelta(hours=24)
    Visit.objects.filter(status='pending', created_at__lt=cutoff).update(status='expired')

@shared_task
def auto_checkout_overdue():
    now = timezone.now()
    overdue = Visit.objects.filter(status='checked_in', check_out_at__isnull=True)
    for v in overdue:
        deadline = v.checked_in_at + timedelta(minutes=v.expected_duration_mins + 30)
        if now > deadline:
            v.status = 'check_out'
            v.check_out_at = now
            v.save(update_fields=['status', 'check_out_at'])