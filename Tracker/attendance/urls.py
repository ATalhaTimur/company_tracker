from django.urls import path
from .views import CheckInView, CheckOutView, AttendanceRecordsView
from .api_views import CheckInAPIView, CheckOutAPIView, AttendanceRecordsAPIView

urlpatterns = [
    # Frontend views
    path('check-in/', CheckInView.as_view(), name='attendance-check-in'),
    path('check-out/', CheckOutView.as_view(), name='attendance-check-out'),
    path('records/', AttendanceRecordsView.as_view(), name='attendance-records'),

    # Backend API endpoints
    path('api/check-in/', CheckInAPIView.as_view(), name='api-check-in'),
    path('api/check-out/', CheckOutAPIView.as_view(), name='api-check-out'),
    path('api/records/', AttendanceRecordsAPIView.as_view(), name='api-attendance-records'),
]
