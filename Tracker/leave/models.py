from django.db import models

# Create your models here.
from django.db import models
from accounts.models import CustomUser

class LeaveRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    manager_comments = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Toplam izin günlerini hesapla
        self.total_days = (self.end_date - self.start_date).days + 1
        super().save(*args, **kwargs)
