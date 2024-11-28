from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import WorkReport

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reports'] = WorkReport.objects.filter(user=self.request.user)
        return context


class ReportsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "manager":
            reports = WorkReport.objects.all().values('user__username', 'month', 'total_work_hours', 'total_late_hours', 'leave_days_used')
        else:
            reports = WorkReport.objects.filter(user=request.user).values('month', 'total_work_hours', 'total_late_hours', 'leave_days_used')
        return Response(reports, status=200)