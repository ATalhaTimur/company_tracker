from django.urls import path
from .views import LoginView, LogoutView, RegisterView
from .views import DashboardView
from .api_views import LoginAPIView, LogoutAPIView, RegisterAPIView, ProfileAPIView
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/profile/', ProfileAPIView.as_view(), name='api-profile'),
]
