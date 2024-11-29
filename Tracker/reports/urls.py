from django.urls import path
from .views import ReportsAPI, ReportsView
from .api_views import ReportsAPIView

urlpatterns = [
    # Görüntüleme için template-based endpoint
    path('reports/view/', ReportsView.as_view(), name='view-reports'),

    # API endpointleri
    path('reports/api/', ReportsAPI.as_view(), name='reports-api'),  # Orijinal API endpoint
    path('api/reports/', ReportsAPIView.as_view(), name='reports-api-v2'),  # Yeni backend API
]
