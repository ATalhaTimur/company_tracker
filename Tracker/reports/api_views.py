from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils.dateparse import parse_date
from .models import WorkReport
from accounts.models import CustomUser


class ReportsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Raporları listeleme"""
        if request.user.role == "manager":
            reports = WorkReport.objects.all().values(
                'id', 'user__username', 'month', 'total_work_hours', 'total_late_hours', 'leave_days_used'
            )
        else:
            reports = WorkReport.objects.filter(user=request.user).values(
                'id', 'month', 'total_work_hours', 'total_late_hours', 'leave_days_used'
            )
        return Response(list(reports), status=200)

    def post(self, request):
        """Yeni rapor oluşturma veya mevcut raporu güncelleme"""
        if request.user.role != "manager":
            return Response({"error": "Unauthorized"}, status=403)

        user_id = request.data.get("user_id")
        month = request.data.get("month")
        total_work_hours = request.data.get("total_work_hours", 0)
        total_late_hours = request.data.get("total_late_hours", 0)
        leave_days_used = request.data.get("leave_days_used", 0)

        # Doğrulama
        if not user_id or not month:
            return Response({"error": "User ID and month are required"}, status=400)

        user = CustomUser.objects.filter(id=user_id).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        # Tarih formatını doğrulama
        parsed_month = parse_date(month)
        if not parsed_month:
            return Response({"error": "Invalid date format, expected YYYY-MM-DD"}, status=400)

        # Rapor oluştur veya güncelle
        report, created = WorkReport.objects.update_or_create(
            user=user,
            month=parsed_month,
            defaults={
                "total_work_hours": total_work_hours,
                "total_late_hours": total_late_hours,
                "leave_days_used": leave_days_used,
            },
        )

        if created:
            return Response({"message": "Report created successfully"}, status=201)
        return Response({"message": "Report updated successfully"}, status=200)

    def delete(self, request):
        """Belirli bir raporu silme"""
        if request.user.role != "manager":
            return Response({"error": "Unauthorized"}, status=403)

        report_id = request.data.get("report_id")
        if not report_id:
            return Response({"error": "Report ID is required"}, status=400)

        report = WorkReport.objects.filter(id=report_id).first()
        if not report:
            return Response({"error": "Report not found"}, status=404)

        report.delete()
        return Response({"message": "Report deleted successfully"}, status=200)
