from celery import shared_task
from accounts.models import CustomUser
from notifications.models import Notification


@shared_task
def notify_low_leave_days():
    # 3 günden az yıllık izni kalan personelleri sorgula
    users = CustomUser.objects.filter(annual_leave_days__lte=3, role="personnel")
    # Tüm yöneticileri sorgula
    managers = CustomUser.objects.filter(role="manager")

    for user in users:
        # Personel için bildirim
        Notification.objects.create(
            recipient=user,
            message=f"Attention: Your remaining annual leave days are {user.annual_leave_days}."
        )

        # Her yöneticiye bildirim
        for manager in managers:
            Notification.objects.create(
                recipient=manager,
                message=f"{user.username} has only {user.annual_leave_days} annual leave days remaining."
            )
