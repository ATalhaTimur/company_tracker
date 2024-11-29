from django.shortcuts import redirect
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.views.generic.base import RedirectView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import CustomUser

class LogoutView(RedirectView):
    permanent = False
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return super().get(request, *args, **kwargs)

class LoginView(TemplateView):
    template_name = "login.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("dashboard")
        messages.error(request, "Invalid username or password!")
        return self.get(request, *args, **kwargs)

class RegisterView(TemplateView):
    template_name = "register.html"

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        role = request.POST.get("role", "personnel")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return self.get(request, *args, **kwargs)

        try:
            CustomUser.objects.create_user(username=username, password=password, role=role)
            messages.success(request, "Registration successful! You can now log in.")
            return redirect("login")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return self.get(request, *args, **kwargs)

class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        if self.request.user.role == "personnel":
            return "dashboard/dashboard_personnel.html"
        elif self.request.user.role == "manager":
            return "dashboard/dashboard_manager.html"
        else:
            messages.error(self.request, "Unauthorized access!")
            return redirect('home')
