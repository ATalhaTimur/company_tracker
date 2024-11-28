from datetime import timedelta, datetime
from django.db import models
from accounts.models import CustomUser

class AttendanceRecord(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    check_in_time = models.TimeField()
    check_out_time = models.TimeField(null=True, blank=True)
    late_duration = models.DurationField(null=True, blank=True)

    def save(self, *args, **kwargs):
        work_start_time = datetime.strptime("08:00", "%H:%M").time()
        if self.check_in_time and self.check_in_time > work_start_time:
            late_minutes = (
                                   datetime.combine(self.date, self.check_in_time) - datetime.combine(self.date,
                                                                                                      work_start_time)
                           ).seconds // 60
            self.late_duration = timedelta(minutes=late_minutes)

            # Birikmiş gecikme süresi ekleme
            if late_minutes > 0:
                late_hours = late_minutes / 60
                self.user.annual_leave_days -= int(late_hours // 10)  # 10 saat = 1 gün
                self.user.remaining_late_hours = late_hours % 10  # Kalan saat
                self.user.save()
        super().save(*args, **kwargs)

