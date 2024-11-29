from django.urls import path
from .views import NotificationsAPIView  # API için kullanılıyor
from django.views.generic import TemplateView  # Frontend için basit bir TemplateView

urlpatterns = [
    # Frontend için
    path('view/', TemplateView.as_view(template_name="notifications/notifications.html"), name='notifications'),
    # Backend API için
    path('api/', NotificationsAPIView.as_view(), name='api-notifications'),
]
