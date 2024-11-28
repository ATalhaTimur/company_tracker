from django.urls import path
from .views import CheckInView, CheckOutView, AttendanceRecordsView

urlpatterns = [
    path('check-in/', CheckInView.as_view(), name='api-check-in'),
    path('check-out/', CheckOutView.as_view(), name='api-check-out'),
    path('records/', AttendanceRecordsView.as_view(), name='api-attendance-records'),
]
