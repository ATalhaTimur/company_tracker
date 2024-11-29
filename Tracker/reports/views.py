from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from .models import WorkReport

class ReportsView(LoginRequiredMixin, TemplateView):
    template_name = "reports/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.role == "manager":
            context['reports'] = WorkReport.objects.all()
        else:
            context['reports'] = WorkReport.objects.filter(user=self.request.user)

        return context

class ReportsAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "manager":
            reports = WorkReport.objects.all().values(
                'user__username', 'month', 'total_work_hours', 'total_late_hours', 'leave_days_used'
            )
        else:
            reports = WorkReport.objects.filter(user=request.user).values(
                'month', 'total_work_hours', 'total_late_hours', 'leave_days_used'
            )
        return Response(reports, status=200)

    def post(self, request):
        if request.user.role != "manager":
            return Response({"error": "Unauthorized"}, status=403)

        user_id = request.data.get("user_id")
        month = request.data.get("month")
        total_work_hours = request.data.get("total_work_hours", 0)
        total_late_hours = request.data.get("total_late_hours", 0)
        leave_days_used = request.data.get("leave_days_used", 0)

        # Doğrulama ve oluşturma
        if not user_id or not month:
            return Response({"error": "User ID and month are required"}, status=400)

        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        report, created = WorkReport.objects.update_or_create(
            user=user,
            month=month,
            defaults={
                "total_work_hours": total_work_hours,
                "total_late_hours": total_late_hours,
                "leave_days_used": leave_days_used,
            },
        )

        if created:
            return Response({"message": "Report created successfully"}, status=201)
        return Response({"message": "Report updated successfully"}, status=200)
