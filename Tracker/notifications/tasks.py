from celery import shared_task
from accounts.models import CustomUser
from notifications.models import Notification

@shared_task
def notify_low_leave_days():
    users = CustomUser.objects.filter(annual_leave_days__lte=3)
    for user in users:
        Notification.objects.create(
            recipient=user,
            message=f"Attention: Your remaining annual leave days are {user.annual_leave_days}."
        )
