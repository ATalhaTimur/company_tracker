from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
import logging

logger = logging.getLogger(__name__)

class CheckInView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/check_in.html"

    def post(self, request, *args, **kwargs):
        # Backend'e yönlendirme yap
        messages.success(request, "Check-in request sent successfully!")
        return redirect('attendance-check-in')


class CheckOutView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/check_out.html"

    def post(self, request, *args, **kwargs):
        # Backend'e yönlendirme yap
        messages.success(request, "Check-out request sent successfully!")
        return redirect('attendance-check-out')


class AttendanceRecordsView(LoginRequiredMixin, TemplateView):
    template_name = "attendance/attendance_records.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['records'] = AttendanceRecord.objects.filter(user=self.request.user)
        return context
