from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('personnel', 'Personnel'),
        ('manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='personnel')
    annual_leave_days = models.PositiveIntegerField(default=15)
    remaining_late_hours = models.FloatField(default=0.0)  # Yeni alan

    def __str__(self):
        return self.username

    def can_request_leave(self, requested_days):
        total_hours_available = (self.annual_leave_days * 10) + self.remaining_late_hours
        requested_hours = requested_days * 10
        return total_hours_available >= requested_hours

