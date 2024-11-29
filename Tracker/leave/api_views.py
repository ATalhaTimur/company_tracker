from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest
from django.utils.dateparse import parse_date
import logging

logger = logging.getLogger(__name__)

class LeaveRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        reason = request.data.get("reason", "")

        if not start_date or not end_date:
            return Response({"error": "Start and end dates are required"}, status=400)

        start_date_parsed = parse_date(start_date)
        end_date_parsed = parse_date(end_date)
        if not start_date_parsed or not end_date_parsed:
            return Response({"error": "Invalid date format, use YYYY-MM-DD"}, status=400)

        if start_date_parsed > end_date_parsed:
            return Response({"error": "Start date cannot be after end date"}, status=400)

        LeaveRequest.objects.create(
            user=user,
            start_date=start_date_parsed,
            end_date=end_date_parsed,
            reason=reason
        )
        return Response({"message": "Leave request submitted successfully"}, status=201)


class MyLeaveRequestsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        leave_requests = LeaveRequest.objects.filter(user=user).values(
            'id', 'start_date', 'end_date', 'status', 'reason'
        )
        return Response(list(leave_requests), status=200)


class ApproveLeaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if getattr(request.user, "role", None) != "manager":
            return Response({"error": "Unauthorized"}, status=403)

        pending_requests = LeaveRequest.objects.filter(status="pending").values(
            'id', 'user__username', 'start_date', 'end_date', 'reason'
        )
        return Response(list(pending_requests), status=200)

    def post(self, request):
        if getattr(request.user, "role", None) != "manager":
            return Response({"error": "Unauthorized"}, status=403)

        leave_id = request.data.get("leave_id")
        action = request.data.get("action")

        if action not in ["approve", "reject"]:
            return Response({"error": "Invalid action. Use 'approve' or 'reject'"}, status=400)

        try:
            leave_request = LeaveRequest.objects.get(id=leave_id, status="pending")
            leave_request.status = action
            leave_request.save()
            return Response({"message": f"Leave request {action}d successfully."}, status=200)
        except LeaveRequest.DoesNotExist:
            return Response({"error": "Leave request not found or already processed."}, status=404)
