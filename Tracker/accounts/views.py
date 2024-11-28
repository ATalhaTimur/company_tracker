from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import render
from attendance.models import AttendanceRecord
from leave.models import LeaveRequest
from django.views.generic import TemplateView

from django.shortcuts import render
from attendance.models import AttendanceRecord
from leave.models import LeaveRequest
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework.decorators import api_view

class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role", "personnel")
        user = CustomUser.objects.create_user(username=username, password=password, role=role)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.role == "personnel":
            context['attendance_records'] = AttendanceRecord.objects.filter(user=self.request.user)
            context['leave_requests'] = LeaveRequest.objects.filter(user=self.request.user)
        elif self.request.user.role == "manager":
            context['pending_leaves'] = LeaveRequest.objects.filter(status="pending")
        return context