from django.urls import path
from .views import ReportsAPI

urlpatterns = [
    path('api/', ReportsAPI.as_view(), name='api-reports'),
]
