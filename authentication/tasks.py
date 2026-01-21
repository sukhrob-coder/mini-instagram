from datetime import timedelta

from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@shared_task
def cleanup_unverified_users():
    threshold = timezone.now() - timedelta(hours=24)
    deleted_count, _ = User.objects.filter(
        is_verified=False, date_joined__lt=threshold
    ).delete()
    return f"Deleted {deleted_count} unverified users"
