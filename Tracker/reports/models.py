from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser

class WorkReport(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    month = models.DateField()
    total_work_hours = models.PositiveIntegerField(default=0)
    total_late_hours = models.PositiveIntegerField(default=0)
    leave_days_used = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Report for {self.user.username} - {self.month.strftime('%B %Y')}"
