from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


__all__ = []


@shared_task()
def send_feedback_email_task(email_address, message):
    send_mail(
        subject="Feedback",
        message=message,
        from_email=settings.EMAIL_ADMIN,
        recipient_list=[email_address],
        fail_silently=False,
    )
