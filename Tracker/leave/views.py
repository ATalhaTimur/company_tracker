from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from leave.models import LeaveRequest

class LeaveRequestView(LoginRequiredMixin, TemplateView):
    """
    Kullanıcıların izin talebi yapabileceği şablonu yükler.
    """
    template_name = "leave/leave_request.html"

class MyLeaveRequestsView(LoginRequiredMixin, TemplateView):
    """
    Kullanıcının geçmiş izin taleplerini listeleyen şablonu yükler.
    """
    template_name = "leave/my_leave_requests.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['leave_requests'] = LeaveRequest.objects.filter(user=self.request.user)
        return context

class ApproveLeaveView(LoginRequiredMixin, TemplateView):
    """
    Yöneticinin bekleyen izin taleplerini görüntüleyebileceği şablonu yükler.
    """
    template_name = "leave/approve_leave.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "manager":
            context['leave_requests'] = LeaveRequest.objects.filter(status="pending")
        return context
