from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import WorkReport


class ReportsPersonnelView(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports_personnel.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Sadece kendi raporlarını filtrele
        context['reports'] = WorkReport.objects.filter(user=self.request.user).order_by('-month')
        return context


class ReportsManagerView(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports_manager.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Yönetici tüm raporları görebilir
        reports = WorkReport.objects.select_related('user').all().order_by('-month')
        context['reports'] = reports
        return context