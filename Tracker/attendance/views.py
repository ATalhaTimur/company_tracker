from django.views.generic import TemplateView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from datetime import datetime
import logging
from attendance.models import AttendanceRecord

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

class CheckInView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/check_in.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        date = datetime.now().date()
        check_in_time = datetime.now().time()

        try:
            record, created = AttendanceRecord.objects.get_or_create(user=user, date=date)
            if not created:
                messages.error(request, "Check-in already recorded!")
                return redirect('attendance-check-in')

            record.check_in_time = check_in_time
            record.save()
            messages.success(request, "Check-in successful!")
        except Exception as e:
            logger.error(f"Error during Check-In: {str(e)}")
            messages.error(request, "An unexpected error occurred.")
        return redirect('attendance-check-in')


class CheckOutView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/check_out.html"

    def post(self, request, *args, **kwargs):
        user = request.user
        date = datetime.now().date()
        check_out_time = datetime.now().time()

        try:
            record = AttendanceRecord.objects.get(user=user, date=date)
            if record.check_out_time:
                messages.error(request, "Check-out already recorded!")
                return redirect('attendance-check-out')

            record.check_out_time = check_out_time
            record.save()
            messages.success(request, "Check-out successful!")
        except AttendanceRecord.DoesNotExist:
            messages.error(request, "No check-in record found for today!")
        except Exception as e:
            logger.error(f"Error during Check-Out: {str(e)}")
            messages.error(request, "An unexpected error occurred.")
        return redirect('attendance-check-out')

class AttendanceRecordsView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/attendance_records.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = AttendanceRecord.objects.filter(user=self.request.user)
        return context
