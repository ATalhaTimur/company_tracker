from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from accounts.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=200)
        return Response({"error": "Invalid credentials"}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(APIView):
    def get(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=200)

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role", "personnel")

        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=400)

        try:
            user = CustomUser.objects.create_user(username=username, password=password, role=role)
            return Response({"message": "User registered successfully"}, status=201)
        except Exception as e:  # Bu kısmı sadece kritik hata mesajlarıyla daraltabilirsiniz.
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "role": user.role,
            "annual_leave_days": user.annual_leave_days,
            "remaining_late_hours": user.remaining_late_hours,
        }, status=200)
