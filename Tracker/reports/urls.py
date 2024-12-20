from django.urls import path

from .api_views import ReportsAPIView
from .views import ReportsPersonnelView, ReportsManagerView

urlpatterns = [
    # front-end views
    path('my/', ReportsPersonnelView.as_view(), name='personnel-reports'),
    path('manager/', ReportsManagerView.as_view(), name='reports-manager'),

    # back-end API
    path('api/reports/', ReportsAPIView.as_view(), name='reports-api-v2'),
]
