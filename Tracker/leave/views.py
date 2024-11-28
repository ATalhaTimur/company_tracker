from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import LeaveRequest

class LeaveRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        reason = request.data.get("reason", "")
        LeaveRequest.objects.create(user=user, start_date=start_date, end_date=end_date, reason=reason)
        return Response({"message": "Leave request submitted"}, status=201)

class MyLeaveRequestsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        requests = LeaveRequest.objects.filter(user=user).values('start_date', 'end_date', 'status', 'reason')
        return Response(requests, status=200)



class ApproveLeaveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "manager":
            pending_requests = LeaveRequest.objects.filter(status="pending").values('id', 'user__username', 'start_date', 'end_date', 'reason')
            return Response(pending_requests, status=200)
        return Response({"error": "Unauthorized"}, status=403)

    def post(self, request):
        if request.user.role == "manager":
            leave_id = request.data.get("leave_id")
            action = request.data.get("action")  # "approve" veya "reject"
            try:
                leave_request = LeaveRequest.objects.get(id=leave_id, status="pending")
                if action == "approve":
                    leave_request.status = "approved"
                elif action == "reject":
                    leave_request.status = "rejected"
                leave_request.save()
                return Response({"message": f"Leave request {action}ed successfully."}, status=200)
            except LeaveRequest.DoesNotExist:
                return Response({"error": "Leave request not found or already processed."}, status=404)
        return Response({"error": "Unauthorized"}, status=403)
